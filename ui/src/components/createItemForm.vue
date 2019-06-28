<template>
  <div>
    <form novalidate @submit.prevent="validateItem">
      <md-card class="md-layout-item md-size-90">
        <md-card-header>
          <div class="md-title" v-html="form.name"></div>
        </md-card-header>

        <md-card-content>
          <md-input name="id" v-model="form.id" hidden/>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('title')">
                <label for="title">Title</label>
                <md-input name="title" id="title" v-model="form.title" :disabled="sending"/>
                <span class="md-error" v-if="!$v.form.title.required">The title is required</span>
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('description')">
                <label for="description">Description</label>
                <md-input
                  name="description"
                  id="description"
                  v-model="form.description"
                  :disabled="sending"
                />
                <span
                  class="md-error"
                  v-if="!$v.form.description.minlength"
                >Description min length is 10 character</span>
              </md-field>
            </div>
          </div>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('ranking')">
                <label for="ranking">Ranking</label>
                <md-input
                  type="number"
                  name="ranking"
                  id="ranking"
                  v-model="form.ranking"
                  md-dense
                  :disabled="sending"
                />

                <span class="md-error" v-if="!$v.form.ranking.maxvalue">Ranking maxvalue is 100</span>
                <span class="md-error" v-else-if="!$v.form.ranking.required">Ranking is required</span>
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-100">
              <md-field :class="getValidationClass('category')">
                <label for="category">Category</label>
                <md-select
                  type="text"
                  id="category"
                  name="category"
                  v-model="form.category"
                  :disabled="sending"
                >
                  <md-option
                    v-bind:key="category.id"
                    v-for="category in p_categories"
                    :value="category.id"
                  >{{category.name}}</md-option>
                </md-select>
                <span class="md-error" v-if="!$v.form.category.required">The age is required</span>
              </md-field>
            </div>
          </div>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-50" v-if="form.cDate">
              <md-field>
                <label for="cDate">Created date</label>
                <md-input
                  type="text"
                  name="cDate"
                  id="cDate"
                  v-model="form.cDate"
                  md-dense
                  disabled
                />
              </md-field>
            </div>

            <div class="md-layout-item md-small-size-50" v-if="form.mDate">
              <md-field>
                <label for="ranking">Modified date</label>
                <md-input
                  type="text"
                  name="mDate"
                  id="mDate"
                  v-model="form.mDate"
                  md-dense
                  disabled
                />
              </md-field>
            </div>
          </div>
          <div class="md-layout md-gutter">
            <div class="md-layout-item md-small-size-100">
              <md-table v-if="ifMetadata">
                <md-table-row v-bind:key="index" v-for="(obj, index) in form.metadata">
                  <md-table-cell>
                    <md-field>
                      <label>Select type</label>
                      <md-select v-model="form.metadata[index].type">
                        <md-option selected value="text">Text</md-option>
                        <md-option value="date">Date</md-option>
                        <md-option value="number">Number</md-option>
                        <md-option value="enum">Enum</md-option>
                      </md-select>
                    </md-field>
                  </md-table-cell>
                  <md-table-cell>
                    <md-field>
                      <!-- <label>Key</label> -->
                      <md-input type="text" v-model="form.metadata[index].key"/>
                      <span class="md-helper-text">Key</span>
                    </md-field>
                  </md-table-cell>

                  <md-table-cell>
                    <md-field>
                      <!-- <label>Value</label> -->
                      <md-input
                        v-bind:type="form.metadata[index].type"
                        v-model="form.metadata[index].value"
                      />
                      <span class="md-helper-text">Value</span>
                    </md-field>
                  </md-table-cell>

                  <md-table-cell>
                    <a v-on:click="removeElement(index);" style="cursor: pointer">
                      <md-icon>close</md-icon>
                    </a>
                  </md-table-cell>
                </md-table-row>
              </md-table>
              <div>
                <md-button class="md-raised" @click="addMetadata">Add Metadata</md-button>
              </div>
            </div>
          </div>
        </md-card-content>

        <md-progress-bar md-mode="indeterminate" v-if="sending"/>

        <md-card-actions>
          <md-button
            type="submit"
            class="md-primary"
            :disabled="sending"
            v-html="form.name"
          >Create Item</md-button>
        </md-card-actions>
      </md-card>

      <md-snackbar :md-active.sync="itemSaved">The item {{ lastItem }} was saved with success!</md-snackbar>
    </form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, minLength, maxValue } from "vuelidate/lib/validators";
import axios from "axios";

export default {
  name: "FormCreateItem",
  mixins: [validationMixin],

  props: ["p_categories", "active_item"],
  watch: {
    $props: {
      deep: true,
      immediate: true,
      handler(val, oldVal) {
        this.val = val;
        this.injectItem(this.active_item[0]);
      }
    }
  },
  data: () => ({
    form: {
      name: "Add Item",
      id: null,
      title: null,
      description: null,
      ranking: 0,
      metadata: [],
      metaobj: {},
      category: null,
      cDate: null,
      mDate: null
    },
    payload: {},
    itemSaved: false,
    sending: false,
    lastItem: null,
    val: null
  }),
  validations: {
    form: {
      title: {
        required
      },
      description: {
        minLength: minLength(10)
      },
      ranking: {
        required
      },
      category: {
        required
      }
    }
  },
  created() {},
  methods: {
    injectItem(data) {
      //data = this.item;
      //alert("hi");
      for (var key in data.item_metadata) {
        this.form.metadata.push({
          key: key,
          value: data.item_metadata[key][0],
          type: data.item_metadata[key][1]
        });
      }

      this.form.name = "Edit Item";
      this.form.title = data.title;
      this.form.id = data.id;
      this.form.category_id = data.category_id;
      this.p_categories.forEach(obj => {
        if (obj.id == data.category_id) {
          this.form.category = obj.id;
        }
      });
      this.form.description = data.desc;
      this.form.mDate = data.modified_date;
      this.form.ranking = data.ranking;
      this.form.cDate = data.created_date;
    },
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
      this.form.title = null;
      this.form.description = null;
      this.form.ranking = 0;
      this.form.metadata = [];
      this.form.metaobj = {};
      this.form.cDate = null;
      this.form.mDate = null;
      this.form.category = null;
    },
    saveItem() {
      this.sending = true;
      this.form.metadata.forEach(each => {
        this.form.metaobj[each.key] = [each.value, each.type];
      });
      this.payload = {
        title: this.form.title,
        description: this.form.description,
        ranking: this.form.ranking,
        item_meta: this.form.metaobj,
        category_id: this.form.category
      };
      var axios_method = "post";
      var url = "http://localhost:5000/item";

      if (this.form.id !== null) {
        axios_method = "put";
        url = "http://localhost:5000/item/" + this.form.id;
      }
      axios({
        method: axios_method, //you can set what request you want to be
        url: url,
        data: this.payload,
        headers: {
          "Content-Type": "application/json"
        }
      })
        .then(response => {
          this.lastItem = `${this.form.title}`;
          this.itemSaved = true;
          this.sending = false;
          this.clearForm();
        })
        .catch(error => {
          this.itemSaved = false;
          this.sending = false;
        });
    },
    validateItem() {
      this.$v.$touch();

      if (!this.$v.$invalid) {
        this.saveItem();
      }
    },

    ifMetadata() {
      this.form.metadata.length == 0;
    },
    addMetadata() {
      this.form.metadata.push({
        type: "text",
        key: null,
        value: null
      });
    },
    removeElement(index) {
      this.form.metadata.splice(index, 1);
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
