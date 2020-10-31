<template lang="html">
  <div class="">
    <v-card-title style="width:25%">
      <v-text-field
        v-model="search"
        append-icon="mdi-magnify"
        label="Search Locations"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="locations"
      :items-per-page="10"
      class="elevation-1 "
      :search="search"
    >
      <template v-slot:top>
        <v-toolbar flat color="white">
          <v-toolbar-title class="black--text">Locations</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on }">
              <v-btn color="#5E64FF" dark class="mb-2" v-on="on"
                >New Location</v-btn
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
  </div>
</template>

<script>
import axios from "axios";
const { ip } = require("../config.js");
export default {
  data() {
    return {
      search: "",
      ip: "",
      dialog: false,
      headers: [
        { text: "ID", value: "id", filterable: false },
        { text: "Name", value: "name" },
        {
          text: "Actions",
          value: "action",
          sortable: false,
          filterable: false,
        },
      ],
      locations: [],
      editedIndex: -1,
      editedItem: {
        name: "",
      },
      defaultItem: {
        name: "",
      },
    };
  },
  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "New Location" : "Edit Item";
    },
  },

  created() {
    this.ip = ip;
    this.initialize();
  },
  methods: {
    initialize() {
      //this.locations = [{id:"001",name:"Calden",description:"Lmao"},{id:"002",name:"Alden",description:"LmaoLMAO"}]
      axios
        .get(`${ip}/getLocations`)
        .then((res) => {
          console.log(res.data);
          this.locations = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },

    editItem(item) {
      this.editedIndex = this.locations.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
    },

    deleteItem(item) {
      const id = item.id;
      axios
        .post(`${ip}/delLocation`, { id })
        .then((res) => {
          this.locations = res.data;
          this.text = "Successfully deleted location";
          this.snackbar = true;
        })
        .catch((err) => {
          console.log(err);
          this.text = "Unsuccessfully deleted location";
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
        //Object.assign(this.locations[this.editedIndex], this.editedItem)
        const location = this.editedItem;
        axios
          .post(`${ip}/editLocation`, location)
          .then((res) => {
            this.locations = res.data;
            this.editedItem = Object.assign({}, this.defaultItem);
            this.text = "Successfully edited location";
            this.snackbar = true;
          })
          .catch((err) => {
            console.log(err);
            this.text = "Unsuccessfully edited location";
            this.snackbar = true;
          });
      } else {
        const location = this.editedItem;
        axios
          .post(`${ip}/addLocation`, location)
          .then((res) => {
            //console.log(res.data)
            this.locations = res.data;
            this.editedItem = Object.assign({}, this.defaultItem);
            this.text = "Successfully added location";
            this.snackbar = true;
          })
          .catch((err) => {
            console.log(err);
            this.text = "Unsuccessfully added location";
            this.snackbar = true;
          });
      }
      //this.close()
      this.dialog = false;
    },
  },
};
</script>

<style lang="css" scoped></style>
