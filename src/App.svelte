<script>
    import Episode from "./Episode.svelte";

    const episodes = [{
        id: 1, title: 'Episode 22/20'
    }, {
        id: 2, title: "Episode 22/21"
    }]
</script>

<h1>Hallo</h1>
{#each episodes as episode}
    <Episode episodeData={episode}></Episode>
{/each}
