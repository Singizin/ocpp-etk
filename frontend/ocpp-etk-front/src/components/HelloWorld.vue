<template>
  <div class="hello">
    <MessagePair
      v-for="name in uniqMessages"
      :key="name"
      :message-name="name"
    />
  </div>
</template>

<script>
// import MessageInputField from "@/components/MessageInputField";
import MessagePair from "@/components/MessagePair";

export default {
  name: 'HelloWorld',
  components: {MessagePair},
  props: {
    msg: String
  },
  computed: {
    ocppMessages: function () {
      // eslint-disable-next-line no-undef
      return OCPP_MESSAGES;
    },
    uniqMessages: function () {
      return Object.keys(this.ocppMessages).filter(value => !value.endsWith('Response'))
    }
  },
  created() {
    // console.log(Object.entries(this.ocppMessages))
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
