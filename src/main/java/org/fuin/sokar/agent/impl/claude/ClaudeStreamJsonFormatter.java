package org.fuin.sokar.agent.impl.claude;

import java.util.List;
import java.util.Map;
import org.fuin.sokar.agent.api.LogFormatter;
import org.fuin.sokar.wire.Json;

/**
 * Renders Claude's {@code stream-json} output as readable lines.
 * <p>
 * This is the capability the reference implementation declares in YAML and then ignores, writing
 * {@code if effective_agent == "claude"} in the viewer instead. Here it is a method on the agent,
 * so an agent added later either supplies its own formatter or gets plain text - and either way
 * says which, rather than inheriting a decision made about somebody else.
 * <p>
 * Anything unrecognised is passed through unchanged, and anything recognised but unreadable is
 * passed through with a marker. A log viewer that swallowed lines it did not understand would hide
 * exactly the output worth reading when something has gone wrong - and for an unattended run this
 * is the only record there is.
 */
public class ClaudeStreamJsonFormatter implements LogFormatter {

    /**
     * The only line that is dropped: the CLI announces its session at startup and the operator has
     * that information from the task itself. Matched by subtype, because "system" as a category
     * also carries warnings and errors, and those are the lines an unattended run is read for.
     */
    private static final String BENIGN = "init";

    /** Prefixes a line the formatter recognised but could not read, so it is visibly not prose. */
    private static final String UNREADABLE = "[unreadable] ";

    @Override
    public String format(String line) {

        final String trimmed = line.strip();
        if (!trimmed.startsWith("{")) {
            return line;
        }

        final Object parsed;
        try {
            parsed = Json.parse(trimmed);
        } catch (RuntimeException ex) {
            // Not JSON after all, or a partial line. Show it.
            return line;
        }
        if (!(parsed instanceof Map<?, ?> event)) {
            return line;
        }

        return switch (String.valueOf(event.get("type"))) {
            case "assistant" -> text(event, "", line);
            case "user" -> text(event, "> ", line);
            case "result" -> result(event);
            case "system" -> BENIGN.equals(String.valueOf(event.get("subtype"))) ? null : line;
            default -> line;
        };
    }

    private String text(Map<?, ?> event, String prefix, String line) {
        if (!(event.get("message") instanceof Map<?, ?> message)) {
            return UNREADABLE + line;
        }
        if (!(message.get("content") instanceof List<?> content)) {
            return UNREADABLE + line;
        }
        final StringBuilder out = new StringBuilder();
        for (final Object block : content) {
            if (!(block instanceof Map<?, ?> map)) {
                return UNREADABLE + line;
            }
            if (map.get("text") instanceof String value) {
                out.append(value);
            } else if ("tool_use".equals(String.valueOf(map.get("type")))) {
                out.append("[").append(map.get("name")).append("]");
            } else if (map.get("type") instanceof String type) {
                // A block shape this formatter does not render, named by what it calls itself
                // rather than by a guess: the operator sees that something was there.
                out.append("[").append(type).append("]");
            } else {
                return UNREADABLE + line;
            }
        }
        return out.isEmpty() ? UNREADABLE + line : prefix + out;
    }

    private String result(Map<?, ?> event) {
        final Object cost = event.get("total_cost_usd");
        final Object turns = event.get("num_turns");
        final StringBuilder out = new StringBuilder("-- done");
        if (turns != null) {
            out.append(", ").append(number(turns)).append(" turns");
        }
        if (cost != null) {
            out.append(", $").append(cost);
        }
        return out.toString();
    }

    private static String number(Object value) {
        return value instanceof Number n && n.doubleValue() == Math.floor(n.doubleValue())
                ? String.valueOf((long) n.doubleValue())
                : String.valueOf(value);
    }
}
