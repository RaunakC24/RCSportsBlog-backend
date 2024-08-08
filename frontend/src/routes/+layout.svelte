<script>
    import '../app.css';
    import { category } from '../sport-store';
    import Sportsnavbar from '../lib/sportsnavbar.svelte';
    import Pagetitle from '../lib/pagetitle.svelte';

    let sports = []

    category.subscribe(values => sports = values);

</script>

<Pagetitle></Pagetitle>

<Sportsnavbar {sports} />

<slot />

<style>
    :global(body) {
      background: linear-gradient(to right, #e5eff7, #bad8e7, #e5eff7);
    }
  </style>