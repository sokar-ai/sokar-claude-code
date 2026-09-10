package org.fuin.sokar.agent.impl.claude;

import java.util.ArrayList;
import java.util.List;
import org.fuin.sokar.agent.api.ContainerFile;
import org.fuin.sokar.agent.api.ContainerSetup;
import org.fuin.sokar.agent.api.SetupContext;

/**
 * What Claude Code needs in a fresh container before it will run.
 * <p>
 * The endpoint is not used: this agent is told where to send its requests with environment
 * variables, which is the shape it declared. An agent that can only be given a URL writes it into
 * a file here instead.
 * <p>
 * Three files with three different owners, which is why each is produced somewhere else:
 * {@link ClaudeFirstRun} is the agent's own state, {@link ClaudeSettings} is configuration a
 * person would otherwise edit, and {@link AnthropicCredentialFile} is the shape the provider
 * expects a credential in. This class only says which of them a container needs.
 * <p>
 * Only the third needs a credential, and a task without one still needs the other two: whoever
 * logs in inside the container meets the first-run wizard and the bypass-mode warning otherwise,
 * which is the whole reason those two exist.
 */
public class ClaudeContainerSetup implements ContainerSetup {

    @Override
    public List<ContainerFile> files(final SetupContext context) {
        final List<ContainerFile> files = new ArrayList<>();
        files.add(ContainerFile.of(ClaudeFirstRun.FILE,
                ClaudeFirstRun.document(context.workspace())));
        files.add(ContainerFile.of(ClaudeSettings.FILE, ClaudeSettings.document()));
        if (credentialed(context)) {
            files.add(ContainerFile.secret(AnthropicCredentialFile.FILE,
                    AnthropicCredentialFile.document(context.token(),
                            context.credentialType())));
        }
        return List.copyOf(files);
    }

    /**
     * Returns whether this task was given a credential to present.
     * <p>
     * Written empty, the file states an empty key rather than no key, and the CLI fails with it
     * looking exactly like a wrong one.
     *
     * @param context What the agent was told about the task.
     * @return {@code true} when there is a token to write.
     */
    private static boolean credentialed(final SetupContext context) {
        return context.token() != null && !context.token().isBlank();
    }
}
