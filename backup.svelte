<!-- src/routes/+page.svelte -->
<script lang="ts">
import { Button } from "$lib/components/ui/button";
import { Input } from "$lib/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "$lib/components/ui/select";
import { processVideo } from "$lib/api";

let youtubeUrl = "";
let processingMode = "simple";
let error = "";
let loading = false;

async function handleSubmit() {
  if (!youtubeUrl) {
    error = "Please enter a YouTube URL";
    return;
  }
  
  loading = true;
  error = "";
  
  try {
    const result = await processVideo(youtubeUrl, processingMode);
    window.location.href = `/result/${result.youtube_id}`;
  } catch (err) {
    error = err.message || "An error occurred while processing the video";
  } finally {
    loading = false;
  }
}
</script>

<svelte:head>
  <title>YouTube Transcript Processor</title>
</svelte:head>

<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold mb-8">YouTube Transcript Processor</h1>
  
  {#if error}
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
      <span class="block sm:inline">{error}</span>
    </div>
  {/if}
  
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label for="youtube_url" class="block text-sm font-medium text-gray-700">YouTube URL</label>
      <Input type="url" id="youtube_url" bind:value={youtubeUrl} placeholder="https://www.youtube.com/watch?v=..." required />
    </div>
    
    <div>
      <label for="processing_mode" class="block text-sm font-medium text-gray-700">Processing Mode</label>
      <Select bind:value={processingMode}>
        <SelectTrigger class="w-full">
          <SelectValue placeholder="Select a processing mode" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="simple">Simple</SelectItem>
          <SelectItem value="detailed">Detailed</SelectItem>
        </SelectContent>
      </Select>
    </div>
    
    <Button type="submit" disabled={loading}>
      {loading ? "Processing..." : "Process Video"}
    </Button>
  </form>
</div>