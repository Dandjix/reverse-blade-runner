<template>
    <div>
        <h1>choose a lobby</h1>
        <q-table
            style="height: 400px"
            flat bordered
            title="Rooms"
            :rows="lobbies"
            :columns="columns"
            row-key="index"
            virtual-scroll
            />
    </div>
</template>

<script>
    export default{
        data()
        {
            return {
                columns:[
                    { name: 'name', label: 'Room Name', field: 'name', sortable: true },
                    { name: 'min_players', label: 'Minimum player number', field: 'min_players', sortable: true },
                    { name: 'game_duration', label: 'Game duration (s)', field: 'game_duration', sortable: true },
                    { name: 'language', label: 'Language', field: 'language', sortable: true },
                ],
                lobbies : [{
                    name:"La crounquette",
                    min_players : 2,
                    game_duration : 120,
                    language : "french"
                },
                {
                    name:"Zazaland",
                    min_players : 20,
                    game_duration : 1200,
                    language : "deutsch"
                }]
            }
        }
    }
</script>