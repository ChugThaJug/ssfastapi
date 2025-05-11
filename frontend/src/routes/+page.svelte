<script lang="ts">
  import { processVideo } from "$lib/api";
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { goto } from "$app/navigation";

  let youtubeUrl = "";
  let processingMode = "simple";
  let error: string | null = null;
  let isProcessing = false;

  async function handleSubmit() {
    if (!youtubeUrl) {
      error = "Please enter a YouTube URL";
      return;
    }

    error = null;
    isProcessing = true;

    try {
      console.log(`Processing video with URL: ${youtubeUrl} and mode: ${processingMode}`);
      const result = await processVideo(youtubeUrl, processingMode);
      console.log('Video processing result:', result);
      goto(`/video/${result.youtube_id}`);
    } catch (err) {
      console.error('Error processing video:', err);
      error = err instanceof Error ? err.message : "An error occurred while processing the video";
    } finally {
      isProcessing = false;
    }
  }
</script>

<svelte:head>
  <title>Process Video | Stepify</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-4">Process YouTube Video</h1>

  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label for="youtubeUrl" class="block text-sm font-medium text-gray-700">YouTube URL</label>
      <Input type="text" id="youtubeUrl" bind:value={youtubeUrl} placeholder="https://www.youtube.com/watch?v=..." />
    </div>

    <div>
      <label for="processingMode" class="block text-sm font-medium text-gray-700">Processing Mode</label>
      <select
        id="processingMode"
        bind:value={processingMode}
        class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
      >
        <option value="simple">Simple</option>
        <option value="detailed">Detailed</option>
      </select>
    </div>

    <Button type="submit" disabled={isProcessing}>
      {isProcessing ? 'Processing...' : 'Process Video'}
    </Button>
  </form>

  {#if error}
    <div class="mt-4 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline">{error}</span>
    </div>
  {/if}
</div>