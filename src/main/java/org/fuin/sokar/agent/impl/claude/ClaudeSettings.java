package org.fuin.sokar.agent.impl.claude;

import java.util.LinkedHashMap;
import java.util.Map;
import org.fuin.sokar.wire.Json;

/**
 * The settings that stop the CLI asking to be allowed to do what it was started to do.
 * <p>
 * <strong>The dialog exists because of the flag.</strong> Started with
 * {@code --dangerously-skip-permissions}, the CLI opens with a full-screen warning whose default
 * answer is "No, exit" and which asks the operator to accept responsibility for actions taken in
 * bypass mode. It is not a permission prompt, so the flag cannot answer it - and unattended there
 * is nobody to answer it at all, which is a task that starts and then waits at a menu.
 * <p>
 * <strong>Answering it here is defensible in a way it would not be on a person's machine.</strong>
 * The responsibility the dialog asks about is the container's: an unreviewed egress policy, a
 * workspace that is a clone rather than the operator's checkout, and a gate between anything the
 * agent commits and the real upstream. The question was answered when somebody chose to run the
 * agent in a box.
 * <p>
 * <strong>It also keeps the CLI at the version that was installed.</strong> See
 * {@code doc/decisions.md}, "The CLI does not update itself in a task".
 * <p>
 * Kept apart from {@link ClaudeFirstRun}, which answers the wizard, because the two files are
 * different: this is configuration a person would edit, that is state the CLI writes itself.
 */
final class ClaudeSettings {

    /** Where the CLI reads its settings. */
    static final String FILE = "/home/agent/.claude/settings.json";

    private ClaudeSettings() {
        throw new UnsupportedOperationException("Utility class");
    }

    /**
     * Returns the settings document for a container.
     *
     * @return File content.
     */
    static String document() {

        final Map<String, Object> permissions = new LinkedHashMap<>();
        // The mode the task runs in anyway. Setting it here rather than relying on the flag alone
        // means the CLI starts in it rather than being switched into it and asking about it.
        permissions.put("defaultMode", "bypassPermissions");

        final Map<String, Object> root = new LinkedHashMap<>();
        root.put("permissions", permissions);
        // The dialog itself. Without this the mode above is reached by way of the warning rather
        // than instead of it.
        root.put("skipDangerousModePermissionPrompt", true);

        // The version that runs is the pinned one. Left alone, the CLI fetched 2.1.276 within 90
        // seconds of starting 2.1.267 and would run it on the next start - unpinned and unchecked.
        // DISABLE_UPDATES rather than DISABLE_AUTOUPDATER: it also refuses 'claude update', which
        // the agent could otherwise run through its own shell. 'autoUpdates: false' is no answer,
        // the CLI ignores it for a native install.
        final Map<String, Object> env = new LinkedHashMap<>();
        env.put("DISABLE_UPDATES", "1");
        root.put("env", env);
        return Json.write(root);
    }
}
