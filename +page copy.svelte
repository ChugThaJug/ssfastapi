<script lang="ts">
  import { onMount } from "svelte";
  import ChevronRight from "lucide-svelte/icons/chevron-right";
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card";
  import { getContentResult, updateContent } from "$lib/api";
  import TiptapEditor from "$lib/components/TipTapEditor.svelte";

  export let data: { id: string };
  
  let contentResult: any = null;
  let error: string | null = null;
  let summaryEditMode = false;
  let transcriptEditMode = false;
  let tempSummary = "";
  let tempTranscript = "";
  
  onMount(async () => {
    try {
      if (data && data.id) {
        contentResult = await getContentResult(data.id);
        tempSummary = contentResult.summary || "";
        tempTranscript = contentResult.processed_content || "";
      } else {
        throw new Error("Content ID is missing");
      }
    } catch (err) {
      console.error("Error fetching content result:", err);
      error = err instanceof Error ? err.message : "An error occurred while fetching the result";
    }
  });

  function formatContent(content: string) {
    return content.split('\n').map(line => `<p>${line}</p>`).join('');
  }

  async function handleSummaryUpdate(newSummary: string) {
    tempSummary = newSummary;
  }

  async function handleTranscriptUpdate(newTranscript: string) {
    tempTranscript = newTranscript;
  }

  async function saveSummary() {
    try {
      await updateContent(data.id, { summary: tempSummary });
      contentResult.summary = tempSummary;
      summaryEditMode = false;
    } catch (err) {
      console.error("Error updating summary:", err);
      error = err instanceof Error ? err.message : "An error occurred while updating the summary";
    }
  }

  async function saveTranscript() {
    try {
      await updateContent(data.id, { processed_content: tempTranscript });
      contentResult.processed_content = tempTranscript;
      transcriptEditMode = false;
    } catch (err) {
      console.error("Error updating transcript:", err);
      error = err instanceof Error ? err.message : "An error occurred while updating the transcript";
    }
  }

  function toggleSummaryEditMode() {
    if (summaryEditMode) {
      saveSummary();
    } else {
      tempSummary = contentResult.summary || "";
      summaryEditMode = true;
    }
  }

  function toggleTranscriptEditMode() {
    if (transcriptEditMode) {
      saveTranscript();
    } else {
      tempTranscript = contentResult.processed_content || "";
      transcriptEditMode = true;
    }
  }
</script>

<div class="flex min-h-screen bg-background">
  <div class="flex flex-1 flex-col sm:pl-14">
    <main class="flex-1 overflow-y-auto">
      <div class="container mx-auto max-w-6xl px-4 py-6 lg:px-8">
        <div class="mb-6 flex items-center space-x-2 text-sm text-muted-foreground">
          <a href="/" class="hover:text-foreground">Home</a>
          <ChevronRight class="h-4 w-4" />
          <a href="/content" class="hover:text-foreground">Content</a>
          <ChevronRight class="h-4 w-4" />
          <span class="text-foreground">Result</span>
        </div>

        <div class="grid gap-6 lg:grid-cols-[1fr_250px]">
          <div>
            {#if error}
              <Card.Root>
                <Card.Header>
                  <Card.Title class="text-destructive">Error</Card.Title>
                </Card.Header>
                <Card.Content>
                  <p>{error}</p>
                </Card.Content>
              </Card.Root>
            {:else if contentResult}
              <Card.Root>
                <Card.Header>
                  <Card.Title>{contentResult.title}</Card.Title>
                  <Card.Description>Content ID: {contentResult.content_id}</Card.Description>
                </Card.Header>
                <Card.Content>
                  <div class="space-y-4">
                    <div>
                      <h3 id="content-info" class="text-lg font-semibold">Content Information</h3>
                      <p>Content Type: {contentResult.content_type}</p>
                      <p>Processing Type: {contentResult.processing_type}</p>
                      <p>Processing Mode: {contentResult.processing_mode}</p>
                    </div>
                    <div>
                      <h3 id="summary" class="text-lg font-semibold">Summary</h3>
                      <div class="flex justify-between items-center mb-2">
                        <p class="text-sm text-muted-foreground">Click to edit the summary</p>
                        <Button variant="outline" size="sm" on:click={toggleSummaryEditMode}>
                          {summaryEditMode ? "Save" : "Edit"}
                        </Button>
                      </div>
                      {#if summaryEditMode}
                        <TiptapEditor content={tempSummary} onUpdate={handleSummaryUpdate} />
                      {:else}
                        <div class="prose prose-sm max-w-none">
                          {@html formatContent(contentResult.summary || "")}
                        </div>
                      {/if}
                    </div>
                    <div>
                      <h3 id="processed-content" class="text-lg font-semibold">Processed Content</h3>
                      <div class="flex justify-between items-center mb-2">
                        <p class="text-sm text-muted-foreground">Click to edit the processed content</p>
                        <Button variant="outline" size="sm" on:click={toggleTranscriptEditMode}>
                          {transcriptEditMode ? "Save" : "Edit"}
                        </Button>
                      </div>
                      {#if transcriptEditMode}
                        <TiptapEditor content={tempTranscript} onUpdate={handleTranscriptUpdate} />
                      {:else}
                        <div class="prose prose-sm max-w-none">
                          {@html formatContent(contentResult.processed_content || "")}
                        </div>
                      {/if}
                    </div>
                  </div>
                </Card.Content>
              </Card.Root>
            {:else}
              <Card.Root>
                <Card.Header>
                  <Card.Title>Loading...</Card.Title>
                </Card.Header>
                <Card.Content>
                  <p>Fetching content...</p>
                </Card.Content>
              </Card.Root>
            {/if}
          </div>

          <div class="hidden lg:block">
            <div class="sticky top-20">
              <h2 class="mb-4 text-sm font-semibold">On this page</h2>
              <ul class="space-y-2 text-sm">
                {#if contentResult}
                  <li><a href="#content-info" class="text-muted-foreground hover:text-foreground">Content Information</a></li>
                  <li><a href="#summary" class="text-muted-foreground hover:text-foreground">Summary</a></li>
                  <li><a href="#processed-content" class="text-muted-foreground hover:text-foreground">Processed Content</a></li>
                  {#each (contentResult.processed_content || "").split("\n\n") as _, index}
                    <li class="ml-4">
                      <a href={`#paragraph-${index}`} class="text-muted-foreground hover:text-foreground">Paragraph {index + 1}</a>
                    </li>
                  {/each}
                {/if}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</div>

<style>
  :global(.dark) {
    color-scheme: dark;
  }
</style>