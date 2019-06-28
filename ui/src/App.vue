<template>
  <div id="app">
    <md-tabs v-if="showItems">
      <md-tab
        v-bind:key="category.id"
        v-for="category in categories"
        :id="`tab-${category.name}`"
        :md-label="`${category.name}`"
        @click="loadCategory(category.id)"
      ></md-tab>
    </md-tabs>
    <div v-if="showItems">
      <md-dialog-confirm
        :md-active.sync="showDialogue"
        :md-title="this.dialogueMsg"
        md-content
        md-confirm-text="Agree"
        md-cancel-text="Disagree"
        @md-cancel="onCancel"
        @md-confirm="onConfirm"
      />
    </div>
    <div v-if="isStuffsAvailable">
      <md-card v-bind:key="stuff.id" v-for="stuff in stuffs">
        <md-card-header>
          <md-card-header-text>
            <div class="md-title">{{stuff.title}}</div>
            <div class="md-subhead">
              <md-icon>poll</md-icon>
              <span>{{stuff.ranking}}</span>
            </div>
          </md-card-header-text>

          <md-menu md-size="small" md-direction="bottom-end">
            <md-button class="md-icon-button" md-menu-trigger>
              <md-icon>more_vert</md-icon>
            </md-button>

            <md-menu-content md-size="small">
              <md-menu-item md-size="small" @click="deleteCard(stuff.id)">
                <!-- <span>delete</span> -->
                <md-icon>delete</md-icon>
              </md-menu-item>

              <md-menu-item md-size="small" @click="editCard(stuff.id)">
                <!-- <span>edit</span> -->
                <md-icon>edit</md-icon>
              </md-menu-item>
            </md-menu-content>
          </md-menu>
        </md-card-header>
        <md-card-expand>
          <md-card-actions md-alignment="space-between">
            <div></div>
            <md-card-expand-trigger>
              <md-button class="md-icon-button">
                <md-icon>keyboard_arrow_down</md-icon>
              </md-button>
            </md-card-expand-trigger>
          </md-card-actions>

          <md-card-expand-content>
            <md-card-content>{{stuff.desc}}</md-card-content>
          </md-card-expand-content>
        </md-card-expand>
      </md-card>
    </div>
    <md-speed-dial class="md-top-right" md-direction="bottom">
      <md-speed-dial-target class="md-primary">
        <md-icon class="md-morph-initial">add</md-icon>
        <md-icon class="md-morph-final">close</md-icon>
      </md-speed-dial-target>

      <md-speed-dial-content>
        <md-button class="md-icon-button" @click="addItem">
          <md-icon>subject</md-icon>
          <md-tooltip md-direction="left">add item</md-tooltip>
        </md-button>

        <md-button class="md-icon-button" @click="addCatergory">
          <md-icon>category</md-icon>
          <md-tooltip md-direction="left">add category</md-tooltip>
        </md-button>
        <md-button class="md-icon-button" @click="goHome">
          <md-icon>home</md-icon>
          <md-tooltip md-direction="left">home</md-tooltip>
        </md-button>
      </md-speed-dial-content>
    </md-speed-dial>
    <FormCreateItem
      v-bind:p_categories="categories"
      v-bind:active_item="activeItem"
      v-if="makeCreateItemFormVisible"
    />
    <FormCreateCategory @submit="onCategorySubmited" v-if="makeCreateCategoryFormVisible"/>
  </div>
</template>

<script>
import FormCreateItem from "./components/createItemForm.vue";
import FormCreateCategory from "./components/createCategoryForm.vue";
import axios from "axios";

export default {
  name: "app",
  components: {
    FormCreateItem,
    FormCreateCategory
  },
  data: () => ({
    dialogueId: null,
    dialogueAction: null,
    dialogueMsg: null,
    showDialogue: false,
    isStuffsAvailable: true,
    makeCreateItemFormVisible: false,
    makeCreateCategoryFormVisible: false,
    showItems: true,
    activeItem: null,
    itemId: null,
    value: null,
    categories: [],
    stuffs: []
  }),

  created() {
    axios
      .get("http://localhost:5000/category")
      .then(res => {
        this.categories = res.data;
        this.loadCategory(this.categories[0].id);
      })
      .catch(error => {});
  },
  mounted() {
    //this.loadCategory();
  },
  methods: {
    onCategorySubmited(new_category) {
      //alert("hi");
      this.categories = [...this.categories, new_category];
    },
    loadCategory(id) {
      axios
        .get("http://localhost:5000/category/" + id + "/items")
        .then(res => {
          this.stuffs = res.data;
        })
        .catch(error => {});
    },
    editCard(id) {
      //alert(id);
      this.dialogueMsg = "Edit this Item?";
      this.dialogueId = id;
      this.dialogueAction = "EDIT";
      this.showDialogue = true;
      this.itemId = id;
    },
    deleteCard(id) {
      this.dialogueMsg = "Delete this Item?";
      this.dialogueId = id;
      this.dialogueAction = "DELETE";
      this.showDialogue = true;
      this.itemId = id;
    },
    onConfirm() {
      this.value = "Agreed";
      if (this.dialogueAction == "EDIT") {
        this.showItems = false;
        this.makeCreateCategoryFormVisible = false;
        this.makeCreateItemFormVisible = true;
        this.activeItem = this.stuffs.filter(item => item.id == this.itemId);
      } else if (this.dialogueAction == "DELETE") {
        axios
          .delete("http://localhost:5000/item/" + this.itemId)
          .then(res => {
            this.stuffs.splice(
              this.stuffs.findIndex(s => s.id === this.itemId),
              1
            );
          })
          .catch(error => {});
      }
    },
    onCancel() {
      this.value = "Disagreed";
    },
    addCatergory() {
      this.showItems = false;
      this.makeCreateItemFormVisible = false;
      this.makeCreateCategoryFormVisible = true;
    },
    addItem() {
      this.showItems = false;
      this.makeCreateCategoryFormVisible = false;
      this.makeCreateItemFormVisible = true;
    },
    goHome() {
      this.activeItem = null;
      this.showItems = true;
      this.makeCreateItemFormVisible = false;
      this.makeCreateCategoryFormVisible = false;
    }
  }
};
</script>

<style>
.md-card {
  width: 320px;
  margin: 4px;
  display: inline-block;
  vertical-align: top;
}

.md-card-example .md-subhead .md-icon {
  width: 16px;
  min-width: 16px;
  height: 16px;
  font-size: 16px !important;
}
.md-card-example .md-subhead span {
  vertical-align: middle;
}
.md-card-example .card-reservation {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.md-card-example .card-reservation .md-icon {
  margin: 8px;
}
.md-card-example .md-button-group {
  display: flex;
}
.md-card-example .md-button-group .md-button {
  min-width: 60px;
  border-radius: 2px;
}
.md-custom-header-title {
  width: 60%;
  float: left;
}
.md-custom-header-subtitle {
  width: 60%;
  float: left;
}
.md-custom-header {
  padding-right: 0%;
}
.md-icon-button-custom {
  float: right;
}
</style>
