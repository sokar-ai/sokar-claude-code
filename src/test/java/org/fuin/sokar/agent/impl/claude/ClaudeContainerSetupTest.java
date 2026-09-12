package org.fuin.sokar.agent.impl.claude;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

import java.util.List;
import java.util.Map;
import org.fuin.sokar.agent.api.AgentException;
import org.fuin.sokar.agent.api.ContainerFile;
import org.fuin.sokar.wire.Json;
import org.junit.jupiter.api.Test;

/**
 * Tests for {@link ClaudeContainerSetup}.
 */
class ClaudeContainerSetupTest {

    private static final String TOKEN = "sokar_pt_example";

    private List<ContainerFile> files(String type) {
        return withToken(TOKEN, type);
    }

    private List<ContainerFile> withToken(String token, String type) {
        return new ClaudeContainerSetup().files(new org.fuin.sokar.agent.api.SetupContext(
                token, type, "/workspace", "", "anthropic"));
    }

    private List<String> paths(List<ContainerFile> files) {
        return files.stream().map(ContainerFile::path).toList();
    }

    private Map<?, ?> parse(ContainerFile file) {
        return (Map<?, ?>) Json.parse(file.content());
    }

    private ContainerFile named(String path, String type) {
        return files(type).stream().filter(f -> f.path().equals(path)).findFirst().orElseThrow();
    }

    @Test
    void answersTheQuestionsAFreshContainerWouldBeAsked() {

        // Measured: without these the CLI runs its first-run wizard, and the login menu it offers
        // there is part of the wizard rather than any check of the credential.
        final Map<?, ?> config = parse(named(ClaudeFirstRun.FILE, "oauth"));

        assertThat(config.get("hasCompletedOnboarding")).isEqualTo(Boolean.TRUE);
        assertThat(((Map<?, ?>) ((Map<?, ?>) config.get("projects")).get("/workspace"))
                .get("hasTrustDialogAccepted")).isEqualTo(Boolean.TRUE);
    }

    @Test
    void answersTheBypassModeWarningThatTheFlagItselfCauses() {

        // Reported from a clean machine: started with --dangerously-skip-permissions, the CLI
        // opens with a full-screen warning whose default answer is "No, exit". It is not a
        // permission prompt, so the flag cannot answer it, and unattended nobody can.
        final Map<?, ?> settings = parse(named(ClaudeSettings.FILE, "oauth"));

        assertThat(((Map<?, ?>) settings.get("permissions")).get("defaultMode"))
                .isEqualTo("bypassPermissions");
        assertThat(settings.get("skipDangerousModePermissionPrompt")).isEqualTo(Boolean.TRUE);
    }

    @Test
    void keepsTheSettingsReadableRatherThanSecret() {

        // Configuration, not a credential: nothing in it is worth hiding, and marking it
        // owner-only would say it was.
        assertThat(named(ClaudeSettings.FILE, "oauth").ownerOnly()).isFalse();
        // Beside the credential file, not on top of it. Both live under ~/.claude and writing
        // one where the other goes would take the token with it.
        assertThat(ClaudeSettings.FILE).isNotEqualTo(AnthropicCredentialFile.FILE);
    }

    @Test
    void storesAnOauthTokenWhereItsOwnLoginWould() {
        final Map<?, ?> credentials = parse(named(AnthropicCredentialFile.FILE, "oauth"));

        assertThat(((Map<?, ?>) credentials.get("claudeAiOauth")).get("accessToken"))
                .isEqualTo(TOKEN);
    }

    @Test
    void storesAnApiKeyInItsOwnShape() {

        // The two kinds live in different places in that file; writing one as the other fails
        // looking exactly like a wrong key.
        final Map<?, ?> credentials = parse(named(AnthropicCredentialFile.FILE, "api-key"));

        assertThat(credentials.get("apiKey")).isEqualTo(TOKEN);
        assertThat(credentials.get("claudeAiOauth")).isNull();
    }

    @Test
    void keepsTheCredentialFileToItsOwner() {

        // It holds the task's token. The other file holds no secret and must stay readable.
        assertThat(named(AnthropicCredentialFile.FILE, "oauth").ownerOnly()).isTrue();
        assertThat(named(ClaudeFirstRun.FILE, "oauth").ownerOnly()).isFalse();
    }

    @Test
    void roundTripsThroughItsOwnExtractor() {

        // What is written must be what the extractor reads: the two are the same knowledge,
        // and nothing else in Sokar can catch them drifting apart.
        assertThat(parse(named(AnthropicCredentialFile.FILE, "oauth")).get("claudeAiOauth"))
                .isNotNull();
    }

    @Test
    void placesWhatIsNotACredentialForATaskThatHasNone() {

        // Measured on a VM: none of the three files were placed without a token, so a person
        // logging in inside the container met every dialog these files exist to answer.
        assertThat(paths(withToken("", "oauth")))
                .contains(ClaudeFirstRun.FILE, ClaudeSettings.FILE);
    }

    @Test
    void writesNoCredentialFileWithoutAToken() {

        // Written empty it states an empty key rather than no key, and the CLI fails with it
        // looking exactly like a wrong one.
        assertThat(paths(withToken("   ", "oauth"))).doesNotContain(AnthropicCredentialFile.FILE);
        assertThat(paths(withToken(TOKEN, "oauth"))).contains(AnthropicCredentialFile.FILE);
    }
    @Test
    void refusesACredentialKindThisProviderDoesNotStore() {

        // Everything that was not an API key used to be written as a subscription token, so a new
        // kind, a corrupted record or a typo produced a file in the wrong shape - and the agent
        // then reported an authentication failure, which sends whoever reads it looking at the
        // credential rather than at the mistake.
        assertThatThrownBy(() -> files("subscription"))
                .isInstanceOf(AgentException.class)
                .hasMessageContaining("subscription")
                .hasMessageContaining("api-key")
                .hasMessageContaining("oauth");
    }

    @Test
    void writesBothKindsThisProviderDoesStore() {

        // The other half of the refusal above: the two known kinds still produce their file, so
        // the guard cannot be satisfied by rejecting everything.
        assertThat(named(AnthropicCredentialFile.FILE, "api-key").content()).contains("\"apiKey\"");
        assertThat(named(AnthropicCredentialFile.FILE, "oauth").content())
                .contains("\"claudeAiOauth\"");
    }
}
