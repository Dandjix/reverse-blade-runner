<template>
    <q-card class="chat-card">
        <div class="chat-messages" ref="chatContainer">
            <q-card bordered flat class="message-card"  v-for="(msg,index) in messages" :key="index">
                {{ msg.author }}
                :
                {{ msg.message }}
            </q-card>
        </div>
    </q-card>

    <q-card bordered class="input-card">
        <q-input v-model="messageToSend" @keydown.enter.prevent="send_message">
            <template v-slot:prepend>
                <p class="username-label">{{ username }} : </p>
            </template>
            <template v-slot:append>
                <q-icon name="arrow_drop_up" @click="send_message" class="cursor-pointer" />
            </template>
        </q-input>
    </q-card>
</template>

<style scoped>
    .chat-card{
        width: 100%;
        height: max(50vh,500px);
        margin: 5px;
        border-radius: 40px;
        padding: 50px;
        background: radial-gradient(circle, #ffffff 0%, #555555 100%);
        display: flex;
        flex-direction: column;
    }
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 8px;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    .message-card{
        margin: 20px;
        padding: 20px;
        outline: 2px solid rgb(0, 255, 0);
        background-color: rgba(255,255,255,0.5);
    }
    .input-card{
        padding: 20px;
        margin-top: 20px;
        border-radius: 20px;
    }
    .username-label{
       font-size: 16px;
       height: 100%;
       display: flex;
       flex-direction: column-reverse;
       padding-bottom: 8px;
    }
</style>

<script>
export default{
    data(){
        return {
            messages:[
                {
                    author:"John",
                    message:"Je vais bien."
                },
                {
                    author:"Anton",
                    message:"Did you ever hear the tragedy of Darth Plagueis the wise? No. I thought not, It's No story the jedi would tell you. It's a sith legend. Darth Plagueis was a Dark Lord of the sith. He was so powerful, Yet so wise. He could use the force to influence the medi chlorians to create, Life. He had such a knowledge of the Dark side, He could even keep the ones he cared about, From dying. He could actually, Save the ones he cared about from death? The dark side of the force is a pathway to many abilities some consider to be unnatural. Well what happened to him? Darth Plagueis became so powerful that the only thing he feared was losing his power, Which eventually of course he did. Unfortunately, He taught his apprentice everything he knew. Then his apprentice killed him in his sleep. Ironic, He could save others from death, But not himself. Is it possible to learn this power? Not from a jedi. "
                }
            ],
            username:"John",
            messageToSend:""
        }
    },
    watch: {
        messages: {
            handler() {
                const isAtB = this.isAtBottom()
                console.log("is at bottom ? "+isAtB)
                if (isAtB) {
                    this.$nextTick(() => {
                    this.scrollToBottom();
                    });
                }
            },
            deep: true
        }
    },
    methods:{
        send_message()
        {
            if(!this.messageToSend.trim())
                return

            this.messages.push({
                    author:this.username,
                    message:this.messageToSend
            })
            this.messageToSend = ""
        },
        scrollToBottom() {
            const container = this.$refs.chatContainer;
            if (container) {
                container.scrollTop = container.scrollHeight;
            }
        },
        isAtBottom() 
        {
            const container = this.$refs.chatContainer;
            if (!container) return false;
            const threshold = 20; // px from bottom counts as "at bottom"
            return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
        }
    }
}
</script>