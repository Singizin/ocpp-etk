<template>
  <div class="pair_wrapper">
    <MessageInputField
      :message-name="messageName"
      v-on:send-request="sendRequest"
    />
    <MessageInputField
      :message-name="messageName+'Response'"
      :res-json="resJson"
      is-response-form
    />
  </div>
</template>

<script>
import MessageInputField from "@/components/MessageInputField";

export default {
  name: "MessagePair",
  components: {MessageInputField},
  props: {
    messageName: {
      type: String,
      default: 'Authorize'
    },
  },
  data() {
    return {
      resJson: {
        type: Object,
        default: {}
      }
    }
  },
  methods: {
    async sendRequest(reqJSON) {
      console.log("data from form:", reqJSON)
      // const reqJSON = this.collectInputs()
      if (reqJSON !== false) {
        const response = await fetch("/api",
          {
            method: 'POST',
            // mode: 'no-cors',
            headers: {
              // "Access-Control-Allow-Origin": "http://127.0.0.1:4567",
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(reqJSON)
          });
        const data = await response.json();
        console.log('response: ', data)
        this.resJson = data
      } else {
        // убрать!!! проверку перенести внутрь
        alert('Поля не должны быть пустыми: ' + this.myJson.required.toString())
      }
    },
  }
}
</script>

<style scoped>

.pair_wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
  border-radius: 8px;
  border: 1px darkgrey solid;
  background: lightgray;
  margin: 4px 0;
  max-width: 800px;
}
</style>