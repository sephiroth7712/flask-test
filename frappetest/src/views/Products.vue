<template lang="html">
  <div class="">
    <v-card-title style="width:25%">
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search Products"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="products"
      :items-per-page="10"
      class="elevation-1 white"
      :search="search"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title class="black--text">Products</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>

          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="#5E64FF" dark class="mb-2" v-on="on"
                >New Product</v-btn
              >
            </template>
            <v-card>
              <v-card-title>
                <span class="headline">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.name"
                        label="Name"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="12" sm="6" md="4">
                      <v-text-field
                        v-model="editedItem.description"
                        label="Description"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                <v-btn color="blue darken-1" text @click="save">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.action="{ item }">
        <div>
          <v-icon small class="mr-2" @click="editItem(item)"> edit </v-icon>
          <v-icon small @click="deleteItem(item)"> delete </v-icon>
        </div>
      </template>
    </v-data-table>
    <v-snackbar v-model="snackbar" color="success" :timeout="3000" :top="true">
      {{ text }}
      <v-btn dark text @click="snackbar = false">
        Close
      </v-btn>
    </v-snackbar>
  </div>
</template>
<script>
import axios from "axios";
const { ip } = require("../config.js");
export default {
  data() {
    return {
      search: "",
      snackbar: false,
      text: "",
      ip: "",
      dialog: false,
      headers: [
        { text: "ID", value: "id", filterable: false },
        { text: "Name", value: "name" },
        { text: "Description", value: "description", filterable: false },
        {
          text: "Actions",
          value: "action",
          sortable: false,
          filterable: false,
        },
      ],
      products: [],
      editedIndex: -1,
      editedItem: {
        name: "",
        description: "",
      },
      defaultItem: {
        name: "",
        description: "",
      },
    };
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Product" : "Edit Item";
    },
  },

  created() {
    this.ip = ip;
    this.initialize();
  },
  methods: {
    initialize() {
      axios
        .get(`${ip}/getProducts`)
        .then((res) => {
          this.products = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    editItem(item) {
      this.editedIndex = this.products.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const id = item.id;
      axios
        .post(`${ip}/delProduct`, { id })
        .then((res) => {
          this.products = res.data;
          this.text = "Successfully deleted product";
          this.snackbar = true;
        })
        .catch((err) => {
          console.log(err);
          this.text = "Unsuccessfully deleted product";
          this.snackbar = true;
        });
    },

    close() {
      this.dialog = false;
      this.editedItem = Object.assign({}, this.defaultItem);
      this.editedIndex = -1;
    },

    save() {
      if (this.editedIndex > -1) {
        const product = this.editedItem;
        axios
          .post(`${ip}/editProduct`, product)
          .then((res) => {
            this.products = res.data;
            this.text = "Successfully edited product";
            this.snackbar = true;
          })
          .catch((err) => {
            console.log(err);
            this.text = "Unsuccessfully edited product";
            this.snackbar = true;
          });
      } else {
        const product = this.editedItem;
        axios
          .post(`${ip}/addProduct`, product)
          .then((res) => {
            this.products = res.data;
            this.text = "Successfully added product";
            this.snackbar = true;
          })
          .catch((err) => {
            console.log(err);
            this.text = "Unsuccessfully added product";
            this.snackbar = true;
          });
      }
      this.dialog = false;
    },
  },
};
</script>

<style lang="css" scoped></style>
