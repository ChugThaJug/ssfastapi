<!-- result\[id]\page.svelte (content page) -->

<script lang="ts">
  import { onMount } from "svelte";
  import ChevronRight from "lucide-svelte/icons/chevron-right";
  import Search from "lucide-svelte/icons/search";
  import Package2 from "lucide-svelte/icons/package-2";
  import House from "lucide-svelte/icons/house";
  import Settings from "lucide-svelte/icons/settings";
  import User from "lucide-svelte/icons/user";
  import { Button } from "$lib/components/ui/button/index.js";
  import { Input } from "$lib/components/ui/input/index.js";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu/index.js";
  import * as Tooltip from "$lib/components/ui/tooltip/index.js";
  import { cn } from "$lib/utils.js";
  import { getVideoResult, updateVideoSummary, updateVideoTranscript } from "$lib/api";
  import MainNavbar from "$lib/components/navigation/main-nav.svelte";
  import TiptapEditor from "$lib/components/TipTapEditor.svelte";
  

  import TOC from "$lib/components/toc/table-of-contents.svelte"
  import Tree from "$lib/components/toc/tree.svelte"

  export let data: { id: string };
  
  let videoResult: any = null;
  let error: string | null = null;
  let summaryEditMode = false;
  let transcriptEditMode = false;
  let tempSummary = "";
  let tempTranscript = "";
  
  onMount(async () => {
    try {
      if (data && data.id) {
        videoResult = await getVideoResult(data.id);
        tempSummary = videoResult.summary;
        tempTranscript = videoResult.paragraphs;
      } else {
        throw new Error("Video ID is missing");
      }
    } catch (err) {
      console.error("Error fetching video result:", err);
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
      await updateVideoSummary(data.id, tempSummary);
      videoResult.summary = tempSummary;
      summaryEditMode = false;
    } catch (err) {
      console.error("Error updating summary:", err);
      error = err instanceof Error ? err.message : "An error occurred while updating the summary";
    }
  }

  async function saveTranscript() {
    try {
      await updateVideoTranscript(data.id, tempTranscript);
      videoResult.paragraphs = tempTranscript;
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
      tempSummary = videoResult.summary;
      summaryEditMode = true;
    }
  }

  function toggleTranscriptEditMode() {
    if (transcriptEditMode) {
      saveTranscript();
    } else {
      tempTranscript = videoResult.paragraphs;
      transcriptEditMode = true;
    }
  }
</script>

<div class="flex min-h-screen bg-background">

  
  <div class="flex flex-1 flex-col sm:pl-14">


    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto">
      <div class="container mx-auto max-w-6xl px-4 py-6 lg:px-8">
        <!-- Breadcrumb -->
        <div class="mb-6 flex items-center space-x-2 text-sm text-muted-foreground">
          <a href="/" class="hover:text-foreground">Home</a>
          <ChevronRight class="h-4 w-4" />
          <a href="/transcripts" class="hover:text-foreground">Transcripts</a>
          <ChevronRight class="h-4 w-4" />
          <span class="text-foreground">Result</span>
        </div>

        <!-- Content Grid -->
        <div class="grid gap-6 lg:grid-cols-[1fr_250px]">
          <!-- Main Content Area -->
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
            {:else if videoResult}
              <Card.Root>
                <Card.Header>
                  <Card.Title>{videoResult.title}</Card.Title>
                  <Card.Description>Video ID: {videoResult.youtube_id}</Card.Description>
                </Card.Header>
                <Card.Content>
                  <div class="space-y-4">
                    <div>
                      <h3 id="video-info" class="text-lg font-semibold">Video Information</h3>
                      <p>Processing Mode: {videoResult.processing_mode}</p>
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
                          {@html formatContent(videoResult.summary)}
                        </div>
                      {/if}
                    </div>
                    <div>
                      <h3 id="transcript" class="text-lg font-semibold">Transcript</h3>
                      <div class="flex justify-between items-center mb-2">
                        <p class="text-sm text-muted-foreground">Click to edit the transcript</p>
                        <Button variant="outline" size="sm" on:click={toggleTranscriptEditMode}>
                          {transcriptEditMode ? "Save" : "Edit"}
                        </Button>
                      </div>
                      {#if transcriptEditMode}
                        <TiptapEditor content={tempTranscript} onUpdate={handleTranscriptUpdate} />
                      {:else}
                        <div class="prose prose-sm max-w-none">
                          {@html formatContent(videoResult.paragraphs)}
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
                  <p>Fetching video transcript...</p>
                </Card.Content>
              </Card.Root>
            {/if}
          </div>


          <!-- "On this page" Sidebar -->
          <div class="hidden lg:block">
            <div class="sticky top-20">
              <h2 class="mb-4 text-sm font-semibold">On this page</h2>
              <ul class="space-y-2 text-sm">
                {#if videoResult}
                  <li><a href="#video-info" class="text-muted-foreground hover:text-foreground">Video Information</a></li>
                  <li><a href="#summary" class="text-muted-foreground hover:text-foreground">Summary</a></li>
                  <li><a href="#transcript" class="text-muted-foreground hover:text-foreground">Transcript</a></li>
                  {#each videoResult.paragraphs.split("\n\n") as _, index}
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