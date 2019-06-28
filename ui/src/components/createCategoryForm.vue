<template>
  <div>
    <form novalidate @submit.prevent="validateCategory">
      <md-card class="md-layout-item md-size-90">
        <md-card-header>
          <div class="md-title" v-html="form.name"></div>
        </md-card-header>

        <md-card-content>
          <md-input name="id" v-model="form.id" hidden/>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('category')">
                <label for="category">Category Name</label>
                <md-input
                  name="category"
                  id="category"
                  v-model="form.category"
                  :disabled="sending"
                />
                <span
                  class="md-error"
                  v-if="!$v.form.category.required"
                >The category name is required</span>
              </md-field>
            </div>
          </div>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="sending"/>

        <md-card-actions>
          <md-button type="submit" class="md-primary" :disabled="sending">Create Category</md-button>
        </md-card-actions>
      </md-card>

      <md-snackbar :md-active.sync="itemSaved">The category {{ lastItem }} was saved with success!</md-snackbar>
    </form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  name: "FormCreateCategory",
  mixins: [validationMixin],
  data: () => ({
    form: {
      name: "Add Category",
      id: null,
      category: null,
      cDate: null,
      mDate: null
    },
    payload: {},
    categorySaved: false,
    sending: false,
    lastCategory: null
  }),
  validations: {
    form: {
      category: {
        required
      }
    }
  },
  methods: {
    getValidationClass(fieldName) {
      const field = this.$v.form[fieldName];

      if (field) {
        return {
          "md-invalid": field.$invalid && field.$dirty
        };
      }
    },
    clearForm() {
      this.$v.$reset();
      this.form.category = null;
      this.form.cDate = null;
      this.form.mDate = null;
    },
    saveCategory() {
      this.sending = true;

      this.payload = {
        name: this.form.category
      };
      axios({
        method: "post", //you can set what request you want to be
        url: "http://localhost:5000/category",
        data: this.payload,
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          this.lastItem = `${this.form.category}`;
          this.itemSaved = true;
          this.sending = false;
          this.clearForm();
          this.$emit("submit", response.data);
        })
        .catch(error => {
          this.itemSaved = false;
          this.sending = false;
        });
    },
    validateCategory() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.saveCategory();
      }
    }
  }
};
</script>

<style scoped>
.md-progress-bar {
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
}
</style>
