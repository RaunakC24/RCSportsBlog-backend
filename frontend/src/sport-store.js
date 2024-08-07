import {writable} from 'svelte/store'

export const category = writable([
    {id: 'nfl', name: 'NFL'}, {id: 'nba', name: 'NBA'}, {id: 'college-football', name: 'NCAAF'}
])