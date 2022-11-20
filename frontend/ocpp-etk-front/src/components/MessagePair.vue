<template>
  <div class="pair_wrapper">
    <MessageInputField
      :message-name="messageName"/>
    <MessageInputField
      :message-name="messageName+'Response'"
      hide-button
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
}
</script>

<style scoped>

.pair_wrapper {
  display: flex;
  flex-direction: row;
  justify-content: center;
}
</style>