<script lang="ts">
    import { Button } from "$lib/components/ui/button";
    import { Input } from "$lib/components/ui/input";
    import { Tabs, TabsList, TabsTrigger } from "$lib/components/ui/tabs";
    import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "$lib/components/ui/select";
    import { Switch } from "$lib/components/ui/switch";
    import { Upload, Globe, FileText, Mic, Type } from "lucide-svelte";
    
    let videoUrl = "";
    let language = "English";
    let collection = "Basic Collection";
    let aiEnabled = false;
    
    function handleSubmit() {
        // Handle form submission
        console.log("Submitted:", { videoUrl, language, collection, aiEnabled });
    }
    </script>
    
    <main class="container mx-auto px-4 py-8 max-w-3xl">
        <h1 class="text-4xl font-bold text-center mb-8">Turbocharge your brain and gain knowledge</h1>
    
        <Tabs defaultValue="video" class="w-full mb-6">
            <TabsList class="grid w-full grid-cols-5">
                <TabsTrigger value="video">Video</TabsTrigger>
                <TabsTrigger value="website">Website</TabsTrigger>
                <TabsTrigger value="pdf">PDF</TabsTrigger>
                <TabsTrigger value="recording">Recording</TabsTrigger>
                <TabsTrigger value="text">Text</TabsTrigger>
            </TabsList>
        </Tabs>
    
        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
            <div class="flex items-center space-x-2">
                <Input 
                    type="url" 
                    placeholder="Paste your video link here" 
                    bind:value={videoUrl}
                    class="flex-grow"
                />
                <Button variant="outline" type="button">
                    <Upload class="w-4 h-4 mr-2" />
                    Upload
                </Button>
            </div>
    
            <div class="flex items-center space-x-4">
                <Select bind:value={language}>
                    <SelectTrigger class="w-[180px]">
                        <Globe class="w-4 h-4 mr-2" />
                        <SelectValue placeholder="Language" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="English">English</SelectItem>
                        <SelectItem value="Spanish">Spanish</SelectItem>
                        <SelectItem value="French">French</SelectItem>
                    </SelectContent>
                </Select>
    
                <Select bind:value={collection}>
                    <SelectTrigger class="w-[180px]">
                        <FileText class="w-4 h-4 mr-2" />
                        <SelectValue placeholder="Collection" />
                    </SelectTrigger>
                    <SelectContent>
                        <SelectItem value="Basic Collection">Basic Collection</SelectItem>
                        <SelectItem value="Advanced Collection">Advanced Collection</SelectItem>
                    </SelectContent>
                </Select>
    
                <div class="flex items-center space-x-2">
                    <Switch id="ai-mode" bind:checked={aiEnabled} />
                    <label for="ai-mode">AI Mode</label>
                </div>
    
                <Button type="submit" class="ml-auto">Submit</Button>
            </div>
        </form>
    
        <p class="text-sm text-gray-500 mt-4">Example</p>
    </main>
    
    <footer class="container mx-auto px-4 py-8 mt-auto">
        <nav class="flex justify-center space-x-4 text-sm text-gray-500">
            <a href="#pricing">Pricing</a>
            <a href="#api">API</a>
            <a href="#team">Team</a>
            <a href="#roadmap">Roadmap</a>
            <a href="#terms">Terms of Service</a>
            <a href="#privacy">Privacy Policy</a>
            <Select value={language}>
                <SelectTrigger class="w-[100px]">
                    <Globe class="w-4 h-4 mr-2" />
                    <SelectValue placeholder="Language" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem value="English">English</SelectItem>
                    <SelectItem value="Spanish">Spanish</SelectItem>
                    <SelectItem value="French">French</SelectItem>
                </SelectContent>
            </Select>
        </nav>
    </footer>