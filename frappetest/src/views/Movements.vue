<template lang="html">
  <div id="app">
    <v-app id="inspire">
      <v-container fluid>
        <v-row>
          <v-col cols="12">
            <v-combobox
              v-model="location"
              :items="locations"
              @change="changedLocation"
              item-text="name"
              label="Select a Location"
              color="#5E64FF"
              return-object
              autofocus
              style="width:25%"
            ></v-combobox>
          </v-col>
          <v-col cols="12">
            <v-data-table
              :headers="headers"
              :items="productsLocation"
              :items-per-page="10"
              class="elevation-1 "
            >
              <template v-slot:top>
                <v-toolbar flat color="white">
                  <v-toolbar-title>Products</v-toolbar-title>
                  <v-divider class="mx-4" inset vertical></v-divider>
                  <v-spacer></v-spacer>
                  <v-dialog v-model="importDialog" max-width="500px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="#5E64FF" dark class="ma-2" v-on="on"
                        >Import Product</v-btn
                      >
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">Import Product</span>
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-combobox
                                v-model="productSelected"
                                :items="products"
                                item-text="name"
                                label="Select a Product"
                                color="#5E64FF"
                                return-object
                                autofocus
                              ></v-combobox>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field
                                v-model="quantity"
                                label="Quantity"
                              ></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeImport"
                          >Cancel</v-btn
                        >
                        <v-btn color="blue darken-1" text @click="saveImport"
                          >Save</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <v-dialog v-model="exportDialog" max-width="500px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="#e53935" dark class="ma-2" v-on="on"
                        >Export Product</v-btn
                      >
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">Export Product</span>
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-combobox
                                v-model="productSelected"
                                :items="productsAllowed"
                                item-text="name"
                                label="Select a Product"
                                color="#5E64FF"
                                return-object
                                autofocus
                              ></v-combobox>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field
                                v-model="quantity"
                                label="Quantity"
                                :rules="[rules.quantity]"
                              ></v-text-field>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeExport"
                          >Cancel</v-btn
                        >
                        <v-btn color="blue darken-1" text @click="saveExport"
                          >Save</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                  <v-dialog v-model="moveDialog" max-width="500px">
                    <template v-slot:activator="{ on }">
                      <v-btn color="#fb8c00" dark class="ma-2" v-on="on"
                        >Move Product</v-btn
                      >
                    </template>
                    <v-card>
                      <v-card-title>
                        <span class="headline">Export Product</span>
                      </v-card-title>

                      <v-card-text>
                        <v-container>
                          <v-row>
                            <v-col cols="12">
                              <v-combobox
                                v-model="productSelected"
                                :items="productsAllowed"
                                item-text="name"
                                label="Select a Product"
                                color="#5E64FF"
                                return-object
                                autofocus
                              ></v-combobox>
                            </v-col>
                            <v-col cols="12">
                              <v-text-field
                                v-model="quantity"
                                label="Quantity"
                              ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                              <v-combobox
                                v-model="locationSelected"
                                :items="locationsAllowed"
                                item-text="name"
                                label="Select a Location"
                                color="#5E64FF"
                                return-object
                              ></v-combobox>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-card-text>

                      <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="blue darken-1" text @click="closeMove"
                          >Cancel</v-btn
                        >
                        <v-btn color="blue darken-1" text @click="saveMove"
                          >Save</v-btn
                        >
                      </v-card-actions>
                    </v-card>
                  </v-dialog>
                </v-toolbar>
              </template>
            </v-data-table>
          </v-col>
        </v-row>
      </v-container>
    </v-app>
    <v-snackbar
      v-model="snackbar"
      :color="reportColor"
      :timeout="3000"
      :top="true"
    >
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
      importDialog: false,
      exportDialog: false,
      moveDialog: false,
      snackbar: false,
      reportColor: "red",
      productSelected: "",
      locationSelected: "",
      headers: [
        { text: "ID", value: "pid" },
        { text: "Name", value: "name" },
        { text: "Description", value: "description" },
        { text: "Quantity", value: "quantity" },
      ],
      rules: {
        quantity: (value) => {
          console.log(this.productSelected);
          if (this.productSelected === null) {
            return "Please select a product";
          }
          return (
            (0 < parseInt(value) &&
              parseInt(value) <= parseInt(this.productSelected.quantity)) ||
            `Please enter a number between 1 and ${this.productSelected.quantity}`
          );
        },
      },
      locations: [],
      productsAllowed: [],
      locationsAllowed: [],
      products: [],
      productsLocation: [],
      location: "",
      quantity: 0,
      text: "",
    };
  },
  created() {
    this.ip = ip;
    this.initialize();
  },
  methods: {
    clear() {
      this.productSelected = "";
      this.locationSelected = "";
      this.quantity = 0;
    },
    initialize() {
      axios
        .get(`${ip}/getLocations`)
        .then((res) => {
          this.locations = res.data;
          axios
            .get(`${ip}/getProducts`)
            .then((res) => {
              //   console.log(res.data);
              this.products = res.data;
            })
            .catch((err) => {
              console.log(err);
            });
        })
        .catch((err) => {
          console.log(err);
        });
    },
    changedLocation() {
      if (this.location === null) {
        this.text = "Please select a location";
        this.snackbar = true;
        this.importDialog = false;
        this.exportDialog = false;
        this.moveDialog = false;
        this.reportColor = "red";
        return;
      }

      this.locationsAllowed = this.locations.slice();
      for (var i = 0; i < this.locationsAllowed.length; i++) {
        if (this.locationsAllowed[i].id == this.location.id) {
          this.locationsAllowed.splice(i, 1);
        }
      }

      const location = this.location.id;
      axios
        .post(`${ip}/movements/getProducts`, { location })
        .then((res) => {
          console.log(res.data);
          this.productsLocation = res.data;
          this.productsAllowed = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    },
    closeImport() {
      this.importDialog = false;
    },
    saveImport() {
      if (this.location === null) {
        this.text = "Please select a location";
        this.snackbar = true;
        this.importDialog = false;
        this.reportColor = "red";
        return;
      }
      const type = "import";
      const to_location = this.location.id;
      const product_id = this.productSelected.pid;
      const quantity = this.quantity;
      axios
        .post(`${ip}/movements/importProduct`, {
          type,
          to_location,
          product_id,
          quantity,
        })
        .then((res) => {
          this.productsLocation = res.data;
          this.text = "Successfully imported";
          this.snackbar = true;
          this.reportColor = "success";
          this.clear();
        })
        .catch((err) => {
          console.log(err);
          this.text = "Unsuccessfully imported";
          this.snackbar = true;
          this.reportColor = "red";
        });
      this.importDialog = false;
    },
    closeExport() {
      this.exportDialog = false;
    },
    saveExport() {
      if (this.location === null) {
        this.text = "Please select a location";
        this.snackbar = true;
        this.exportDialog = false;
        this.reportColor = "red";
        return;
      }
      const type = "export";
      const from_location = this.location.id;
      const product_id = this.productSelected.pid;
      const quantity = this.quantity;
      axios
        .post(`${ip}/movements/exportProduct`, {
          type,
          from_location,
          product_id,
          quantity,
        })
        .then((res) => {
          this.productsLocation = res.data;
          this.text = "Successfully exported";
          this.snackbar = true;
          this.reportColor = "success";
          this.clear();
        })
        .catch((err) => {
          console.log(err);
          this.text = "Unsuccessfully exported";
          this.snackbar = true;
          this.reportColor = "red";
        });
      this.exportDialog = false;
    },

    closeMove() {
      this.moveDialog = false;
    },
    saveMove() {
      if (this.location === null) {
        this.text = "Please select a location";
        this.snackbar = true;
        this.moveDialog = false;
        this.reportColor = "red";
        return;
      }
      const type = "move";
      const from_location = this.location.id;
      const product_id = this.productSelected.pid;
      const quantity = this.quantity;
      const to_location = this.locationSelected.id;
      axios
        .post(`${ip}/movements/moveProduct`, {
          type,
          from_location,
          product_id,
          quantity,
          to_location,
        })
        .then((res) => {
          this.productsLocation = res.data;
          this.text = "Successfully moved";
          this.snackbar = true;
          this.reportColor = "success";
          this.clear();
        })
        .catch((err) => {
          console.log(err);
          this.text = "Unsuccessfully moved";
          this.snackbar = true;
          this.reportColor = "red";
        });
      this.moveDialog = false;
    },
    checkQuantity() {},
  },
};
</script>

<style lang="css" scoped></style>
