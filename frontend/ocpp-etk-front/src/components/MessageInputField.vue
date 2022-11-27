<template>
  <div class="message_form">
    <div class="message_title">{{ myJson.title }}</div>
    <div
      v-for="(el,key) in myJson.properties"
      :key="key"
    >
      <div :class="isRequired(key)" class="message_property">
        <div class="message_property_name">{{ key }}</div>
        <input
          v-if="!isResponseForm"
          :type="el.type"
          :maxlength="el.maxlength"
          :required="isRequired(key)"
          v-model="properties[key]"
        >
        <p
          v-if="isResponseForm"
        >{{ properties[key] }}</p>
      </div>
    </div>
    <div class="preview_properties">
      <pre>{{ JSON.stringify(properties, null, 2) }}</pre>
    </div>
    <div
      class="button_wrapper"
      v-if="!isResponseForm"
    >
      <button
        @click="$emit('send-request',collectInputs())"
      >
        Отправить
      </button>
    </div>
  </div>
</template>

<script>

import {toRaw} from "vue";

export default {
  name: 'MessageInputField',
  props: {
    messageName: {
      type: String,
      required: true
    },
    isResponseForm: Boolean,
    resJson: {}
  },
  data() {
    // eslint-disable-next-line no-undef
    const myJson = OCPP_MESSAGES[this.messageName]
    // console.log(this.messageName, myJson)
    return {
      myJson,
      properties: Object.keys(myJson.properties).reduce((acc, prop) => ({...acc, [prop]: null}), {}),
    }
  },
  methods: {
    getKey(object) {
      return Object.keys(object)
    },
    isRequired(key) {
      if (this.myJson.required && [...this.myJson.required].includes(key)) {
        return 'required_input'
      }
      return ''
    },
    collectInputs() {
      // console.log('collectInputs: ', Object.entries(this.myJson.properties))
      const result = {}
      const raw_properties = toRaw(this.properties)

      for (const key of Object.keys(raw_properties)) {
        const value = raw_properties[key]
        console.log('Property: Value= {', key, ':', value, '}')
        if (value !== null) {
          result[key] = value
        } else {
          if (this.isRequired(key)) {
            return false
          }
        }
      }
      console.log('result of collectInputs: ', result)
      return result
    },
    // async sendRequest() {
    //   const reqJSON = this.collectInputs()
    //   if (reqJSON !== false) {
    //     const response = await fetch("/api",
    //       {
    //         method: 'POST',
    //         // mode: 'no-cors',
    //         headers: {
    //           // "Access-Control-Allow-Origin": "http://127.0.0.1:4567",
    //           'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify(reqJSON)
    //       });
    //     const data = await response.json();
    //     console.log('response: ', data)
    //   } else {
    //     alert('Поля не должны быть пустыми: ' + this.myJson.required.toString())
    //   }
    // },
    // reduceCustom(arr) {
    //   let result = {}
    //   for (const el of arr) {
    //     result = {...result, [el]: null}
    //   }
    // },
  },
  watch: {
    resJson: function () {
      console.log('updated resJSON', this.resJson)
      if (this.isResponseForm) {
        for (const key of Object.keys(this.resJson)) {
          console.log(key, Object.keys(this.properties).includes(key))
          if (Object.keys(this.properties).includes(key)) {
            this.properties[key] = this.resJson[key]
          }
        }
      }
    },
    properties: function () {
      this.checkRequiredFields()
    }
  }
}
</script>

<style scoped>

.message_form {
  background: #2c3e50;
  border: 1px solid dimgray;
  border-radius: 4px;
  margin: 4px;
  padding: 4px;
  width: 450px;
}

.message_title {
  font-size: 14px;
  font-weight: bold;
  color: white;
  padding: 4px 0;
}

.message_property_name {
  display: flex;
  font-size: 12px;
  padding: 0 4px;
  color: white;
  align-items: center;
}

.message_property {
  display: flex;
  flex-direction: row;
  justify-content: right;
  padding: 2px 2px;
  border-radius: 2px;
  margin: 2px 0;
}

.message_property > p {
  font-size: 12px;
  margin: 2px 0;
  padding: 2px 2px;
  border-radius: 2px;
  background: white;
  min-width: 150px;
}

.message_property > input {
  border-radius: 2px;
  background: white;
  border: 2px #87b4da solid;
}

.message_property > .required_input {
  background: #456282;
}

.button_wrapper {
  display: flex;
  justify-content: flex-end;
  margin: 2px 0 0 0;
}

button {
  background: #32bd6e;
  border: 1px solid #109a4f;
  border-radius: 2px;
  padding: 4px 4px;
}

button:hover {
  background: #439b6b;
}

button:active {
  background: #78c59a;
}

.required_input {
  background: #456282;
}

.preview_properties {
  background: lightgray;
  border-radius: 2px;
  padding: 2px;
}

.preview_properties > pre {
  text-align: left;
  font-size: 12px;
}


</style>