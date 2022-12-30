<template>
    <v-row justify="center">
      <v-dialog v-model="dogSalonDialog" max-width="1200px">
        <v-card>
          <v-card-title>
            <span class="headline primary--text">{{
              __('Dog Slon')
            }}</span>
          </v-card-title>
          <v-card-text class="pa-0">
            <v-container>
              <v-row>
                <v-col cols="12" class="pa-1">
                  <template>
                    <v-row>
                      <v-col>
                        <v-btn @click="add_salon_data_row()" class="mx-2" dark color="cyan">
                          <v-icon dark>
                            mdi-plus
                          </v-icon>
                        </v-btn>
                      </v-col>
                    </v-row>
                    <v-row v-for="(salon, index) in salon_data" :key="salon.id">
                      <v-col>
                        <v-select :items="pets" item-text="pet_name" item-value="pet_id" :label="frappe._('Customer Pets')" dense outlined
      hide-details v-model="salon.pet" @change="get_selected_pet" background-color="white"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="groomers" item-text="name" item-value="name" :label="frappe._('Groomer')" dense outlined
      hide-details v-model="salon.groomer" @change="get_selected_groomer(salon, index)" background-color="white"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="timeslots" item-text="slot_id" item-value="slot_id" :label="frappe._('Time Slots')" dense outlined
      hide-details v-model="salon.timeslot" @change="get_selected_timeslot" background-color="white" :no-data-text="__('No Time Slot Available')"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="all_services" item-text="service_name" item-value="service_id" :label="frappe._('Services')" dense outlined
      hide-details v-model="salon.services" multiple @change="get_selected_services" background-color="white"></v-select>
                      </v-col>
                      
                    </v-row>
                  </template>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="error" dark @click="close_dog_salon_dialog">{{
              __('Close')
            }}</v-btn>
            <v-btn color="success" dark @click="submit_dog_salon_dialog">{{
              __('Submit')
            }}</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-row>
  </template>
  
<script>
  import { evntBus } from '../../bus';
  export default {
    data: () => ({
      dogSalonDialog: false,
      pets: [],
      groomers: [],
      timeslots: [],
      all_services: [],
      salon_data: [ {
        customer: "",
        pet: "",
        groomer: "",
        timeslot: "",
        services: [],
      }]
    }),
    watch: {},
    methods: {

      get_customer_pets(customer) {
        this.pets = [];
        vm = this;
        frappe.db.get_list("Pet", { fields: ["name", "pet_name"], filters: { customer: customer } }).then((res) => {
          res.forEach(pet => {
            p = { "pet_id": pet.name, "pet_name": pet.pet_name }
            vm.pets.push(p)
          })
        }).catch(e => {
          console.log('Error', e)
        })
      },

      get_selected_pet() {

      },

      get_groomers() {
        this.groomers = [];
        vm = this;
        frappe.db.get_list("Neo Groomer", { fields: ["name"] }).then((res) => {
          res.forEach(groomer=> {
            p = { "name": groomer.name }
            vm.salon_data[index].groomers.push(p)
          })
        }).catch(e => {
          console.log('Error', e)
        })
      },

      get_selected_groomer(salon) {
        this.get_services(salon.groomer);
        this.get_time_slot(salon.groomer);
      },

      get_time_slot(groomer) {
        this.timeslots = [];
        var vm = this;
        frappe.db.get_doc("Neo Groomer", groomer)
          .then(doc => {
            doc.time_slot.forEach(ts => {
              frappe.db.count("Neo Time Slot Booking", filters = { "hair_stylist": groomer, "booking_date": frappe.datetime.now_date(), "start_time": ts.start_time, "end_time": ts.end_time, "booking_for": "Dog Salon" })
                .then((tsb) => {
                  if (tsb >= 1) {
                    
                  } else {
                    slot = { "slot_id": `${ts.start_time} ${ts.end_time}` }
                    vm.salon_data[index].timeslots.push(slot)
                  }
                })
            })
          })
      },

      get_selected_timeslot() {

      },

      get_services(groomer) {
        this.all_services = [];
        vm = this;
        frappe.db.get_list("Neo Groomer Services", { fields: ["service_item", "item_name"], filters: { parent: groomer} }).then((res) => {
          res.forEach(service=> {
            p = { "service_id": service.service_item, "service_name": service.item_name }
            vm.all_services.push(p)
          })
        }).catch(e => {
          console.log('Error', e)
        })
      },

      get_selected_services() {

      },
      
      close_dog_salon_dialog() {
        this.dogSalonDialog = false;
      },

      add_salon_data_row() {
        var obj = {
          pet: this.pet,
          groomer: this.groomer,
          timeslot: this.time_slot,
          services: []
        }
        this.salon_data.push(obj)
      },
  
      submit_dog_salon_dialog() {
        evntBus.$emit('submit_dog_salon_dialog');
        this.dogSalonDialog = false;
      },
      formtCurrency(value) {
        value = parseFloat(value);
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
    },
    created: function () {
      evntBus.$on('open_dog_salon_dialog', (data) => {
        this.dogSalonDialog = true;
        this.customer = data;
        this.get_customer_pets(data);
        this.get_groomers();
      });

      
    },
  };
  </script>
  