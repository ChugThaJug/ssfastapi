<script lang="ts">
    import { onMount } from "svelte";
    import ChevronRight from "lucide-svelte/icons/chevron-right";
    import Search from "lucide-svelte/icons/search";
    import Package2 from "lucide-svelte/icons/package-2";
    import House from "lucide-svelte/icons/house";
    import Settings from "lucide-svelte/icons/settings";
    import User from "lucide-svelte/icons/user";
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import * as Card from "$lib/components/ui/card";
    import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
    import * as Tooltip from "$lib/components/ui/tooltip";
    import { cn } from "$lib/utils";
  
    let categories = [
      {
        title: "Generate images",
        description: "Models that generate images from text prompts",
        models: [
          "bytedance/sdxl-lightning-4step",
          "stability-ai/stable-diffusion",
          "black-forest-labs/flux-schnell"
        ],
        moreCount: 27
      },
      {
        title: "Use a language model",
        description: "Models that can understand and generate text",
        models: [
          "meta/meta-llama-3-70b-instruct",
          "meta/meta-llama-3-8b-instruct",
          "meta/meta-llama-3-8b"
        ],
        moreCount: 38
      },
      {
        title: "Caption images",
        description: "Models that generate text from images",
        models: [
          "salesforce/blip",
          "andreasjansson/blip-2",
          "yorickvp/llava-13b"
        ],
        moreCount: 10
      },
      {
        title: "Edit images",
        description: "Tools for manipulating images.",
        models: [
          "tencentarc/gfpgan",
          "sczhou/codeformer",
          "rossiilian/controlnet"
        ],
        moreCount: 23
      },
      {
        title: "Restore images",
        description: "Models that improve or restore images by deblurring, colorization, and removing noise",
        models: [
          "tencentarc/gfpgan",
          "sczhou/codeformer",
          "jingyunliang/swinir"
        ],
        moreCount: 17
      },
      {
        title: "The FLUX.1 family of models",
        description: "The FLUX.1 family of text-to-image models from Black Forest Labs",
        models: [
          "black-forest-labs/flux-schnell",
          "black-forest-labs/flux-pro",
          "black-forest-labs/flux-dev"
        ],
        moreCount: 1
      },
      {
        title: "Upscale images",
        description: "Upscaling models that create high-quality images from low-quality images",
        models: [
          "nightmareai/real-esrgan",
          "jingyunliang/swinir",
          "philz1337x/clarity-upscaler"
        ],
        moreCount: 19
      },
      {
        title: "Get embeddings",
        description: "Models that generate embeddings from inputs",
        models: [
          "andreasjansson/clip-features",
          "daanelson/imagebind",
          "replicate/all-mpnet-base-v2"
        ],
        moreCount: 5
      },
      {
        title: "Extract text from images",
        description: "Optical character recognition (OCR) and text extraction",
        models: []
      },
      {
        title: "Transcribe speech",
        description: "Models that convert speech to text",
        models: []
      },
      {
        title: "Chat with images",
        description: "Ask language models about images",
        models: []
      },
      {
        title: "Use handy tools",
        description: "Toolbelt-type models for videos and images.",
        models: []
      }
    ];
  
    let searchQuery = "";
  
    function filterCategories(query: string) {
      return categories.filter(category =>
        category.title.toLowerCase().includes(query.toLowerCase()) ||
        category.description.toLowerCase().includes(query.toLowerCase()) ||
        category.models.some(model => model.toLowerCase().includes(query.toLowerCase()))
      );
    }
  
    $: filteredCategories = filterCategories(searchQuery);
  </script>
  
  <div class="flex min-h-screen bg-background">
    <!-- Side Navbar -->
    <aside class="fixed inset-y-0 left-0 z-20 hidden w-14 flex-col border-r sm:flex">
      <nav class="flex flex-col items-center gap-4 px-2 py-5">
        <a href="/" class="flex h-9 w-9 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Package2 class="h-4 w-4" />
          <span class="sr-only">Replicate</span>
        </a>
        <Tooltip.Root>
          <Tooltip.Trigger asChild let:builder>
            <a href="/" class="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground" use:builder.action {...builder}>
              <House class="h-5 w-5" />
              <span class="sr-only">Dashboard</span>
            </a>
          </Tooltip.Trigger>
          <Tooltip.Content side="right">Dashboard</Tooltip.Content>
        </Tooltip.Root>
      </nav>
      <nav class="mt-auto flex flex-col items-center gap-4 px-2 py-5">
        <Tooltip.Root>
          <Tooltip.Trigger asChild let:builder>
            <a href="/settings" class="flex h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground" use:builder.action {...builder}>
              <Settings class="h-5 w-5" />
              <span class="sr-only">Settings</span>
            </a>
          </Tooltip.Trigger>
          <Tooltip.Content side="right">Settings</Tooltip.Content>
        </Tooltip.Root>
      </nav>
    </aside>
    
    <div class="flex flex-1 flex-col sm:pl-14">
      <!-- Header -->
      <header class="sticky top-0 z-30 flex h-16 items-center border-b bg-background px-4 sm:px-6">
        <div class="flex items-center space-x-4">
          <span class="font-semibold">chugthajug</span>
          <span class="text-muted-foreground">⟼</span>
        </div>
        <nav class="ml-8 flex space-x-4">
          <a href="/dashboard" class="text-sm font-medium text-muted-foreground hover:text-foreground">Dashboard</a>
          <a href="/explore" class="text-sm font-medium">Explore</a>
          <a href="/playground" class="text-sm font-medium text-muted-foreground hover:text-foreground">Playground</a>
          <a href="/pricing" class="text-sm font-medium text-muted-foreground hover:text-foreground">Pricing</a>
          <a href="/docs" class="text-sm font-medium text-muted-foreground hover:text-foreground">Docs</a>
          <a href="/blog" class="text-sm font-medium text-muted-foreground hover:text-foreground">Blog</a>
          <a href="/changelog" class="text-sm font-medium text-muted-foreground hover:text-foreground">Changelog</a>
        </nav>
        <div class="ml-auto flex items-center space-x-4">
          <div class="relative">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input type="search" placeholder="Search..." class="w-[200px] pl-8 md:w-[300px]" bind:value={searchQuery} />
          </div>
          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild let:builder>
              <Button variant="ghost" size="icon" class="rounded-full" builders={[builder]}>
                <User class="h-5 w-5" />
                <span class="sr-only">User menu</span>
              </Button>
            </DropdownMenu.Trigger>
            <DropdownMenu.Content align="end">
              <DropdownMenu.Label>My Account</DropdownMenu.Label>
              <DropdownMenu.Separator />
              <DropdownMenu.Item>Profile</DropdownMenu.Item>
              <DropdownMenu.Item>Settings</DropdownMenu.Item>
              <DropdownMenu.Separator />
              <DropdownMenu.Item>Logout</DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Root>
        </div>
      </header>
  
      <!-- Main Content -->
      <main class="flex-1 overflow-y-auto">
        <div class="container mx-auto max-w-7xl px-4 py-8">
          <h1 class="mb-6 text-3xl font-bold">I want to...</h1>
          
          <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {#each filteredCategories as category}
              <Card.Root class="flex flex-col justify-between">
                <div>
                  <Card.Header>
                    <Card.Title>{category.title}</Card.Title>
                    <Card.Description>{category.description}</Card.Description>
                  </Card.Header>
                  <Card.Content>
                    <ul class="space-y-1">
                      {#each category.models as model}
                        <li class="text-sm text-muted-foreground hover:text-foreground">
                          <a href={`/models/${model}`}>{model}</a>
                        </li>
                      {/each}
                      {#if category.moreCount > 0}
                        <li class="text-sm text-muted-foreground">and {category.moreCount} more...</li>
                      {/if}
                    </ul>
                  </Card.Content>
                </div>
                {#if category.models.length > 0}
                  <Card.Footer>
                    <Button variant="outline" size="sm" class="w-full">
                      View all
                    </Button>
                  </Card.Footer>
                {/if}
              </Card.Root>
            {/each}
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