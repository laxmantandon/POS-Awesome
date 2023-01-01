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
                    <v-row v-for="(salon, index) in salon_data" :key="salon.pet">
                      <v-col>
                        <v-select :items="pets" item-text="pet_name" item-value="pet_id" :label="frappe._('Customer Pets')" dense outlined
      hide-details v-model="salon.pet" @change="get_selected_pet" background-color="white"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="groomers" item-text="name" item-value="name" :label="frappe._('Groomer')" dense outlined
      hide-details v-model="salon.groomer" @change="get_selected_groomer(salon)" background-color="white"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="salon.timeslots" item-text="slot_id" item-value="slot_id" :label="frappe._('Time Slots')" dense outlined
      hide-details v-model="salon.timeslot" @change="get_selected_timeslot" background-color="white" :no-data-text="__('No Time Slot Available')"></v-select>
                      </v-col>
                      <v-col>
                        <v-select :items="salon.services" item-text="item_name" item-value="service_item" :label="frappe._('Services')" dense outlined
      hide-details v-model="salon.service" multiple @change="get_selected_services" background-color="white"></v-select>
                      </v-col>
                      <v-col cols="1" v-if="index == 0">
                        <v-btn @click="add_salon_data_row()" class="mx-2" dark color="cyan">
                          <v-icon dark>
                            mdi-plus
                          </v-icon>
                        </v-btn>
                      </v-col>
                      <v-col cols="1" v-if="show_remove_button && index >= 1">
                        <v-btn @click="remove_salon_data_row(salon)" class="mx-2" dark color="error">
                          <v-icon dark>
                            mdi-minus
                          </v-icon>
                        </v-btn>
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
      customer: "",
      pets: [],
      groomers: [],
      salon_data: [ {
        pet: "",
        groomer: "",
        service:"",
        services: [],
        timeslot: "",
        timeslots: [],
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
            vm.groomers.push(p)
          })
        }).catch(e => {
          console.log('Error', e)
        })
      },

      get_selected_groomer(salon) {
        this.get_services(salon);
        this.get_time_slot(salon);
      },

      get_time_slot(salon) {
        var vm = this;
        frappe.db.get_doc("Neo Groomer", salon.groomer)
          .then(doc => {
            doc.time_slot.forEach(ts => {
              frappe.db.count("Neo Time Slot Booking", filters = { "hair_stylist": salon.groomer, "booking_date": frappe.datetime.now_date(), "start_time": ts.start_time, "end_time": ts.end_time, "booking_for": "Dog Salon" })
                .then((tsb) => {
                  if (tsb >= 1) {
                    
                  } else {
                    // var x = moment(frappe.datetime.now_time(), 'hh:mm:ss').diff(moment(ts.start_time, 'hh:mm:ss'), 'hour')
                      slot = { "slot_id": `${ts.start_time} ${ts.end_time}` }
                      vm.salon_data.forEach(d => {
                        if (d.pet == salon.pet) {
                          d.timeslots.push(slot)
                        }
                      })
                  }
                })
            })
          })
      },

      get_selected_timeslot() {

      },

      get_services(salon) {
        // this.all_services = [];
        vm = this;

        frappe.call({
          method: 'posawesome.posawesome.api.neoapi.get_groomer_services',
          args: {
            groomer: salon.groomer,
          },
          callback: (r) => {
            vm.salon_data.forEach(d => {
              r.message.forEach(a => {
                if (d.groomer == salon.groomer) {
                  d.services.push({ "service_item": a.service_item, "item_name": a.item_name });
                }
              })
            })
          },
          error: (e) => {
            console.log(e)
          }
        });

        // frappe.db.get_list("Neo Groomer Services", { fields: ["service_item", "item_name"], filters: { parent: salon.groomer } }).then((res) => {
        //   console.log(res)
        //   vm.salon_data.forEach(d => {
        //     res.forEach(a => {
        //       if (d.groomer == salon.groomer) {
        //         d.services.push({"service_item": a.service_item, "item_name": a.item_name});
        //       }
        //     })
        //   })
        // }).catch(e => {
        //   console.log('Error', e)
        // })
      },

      get_selected_services() {

      },
      
      close_dog_salon_dialog() {
        this.dogSalonDialog = false;
      },

      add_salon_data_row() {
        var obj = {
          pet: "",
          groomer: "",
          timeslot: "",
          services: [],
          timeslots: []
        }

        if (this.pets.length == this.salon_data.length || this.pets.length == 0) {
          
        } else {
          this.salon_data.push(obj)
        }
        
      },

      remove_salon_data_row(salon) {
        this.salon_data = this.salon_data.filter((obj) => obj.pet != salon.pet)
      },
  
      submit_dog_salon_dialog() {
        console.log(this.salon_data)
        vm = this;
        this.salon_data.forEach(pet => {
          pet.service.forEach(item => {
            frappe.db.get_doc("Item", item).then(d => {
              // console.log(d)
              let item1 = {
                item_code: d.item_code,
                item_name: d.item_name,
                qty: 1,
                uom: d.stock_uom,
                stock_uom: d.stock_uom
              }
              evntBus.$emit('add_item', item1);
            });
          })
        })
        // evntBus.$emit('submit_dog_salon_dialog', this.salon_data);
        this.dogSalonDialog = false;
      },
      formtCurrency(value) {
        value = parseFloat(value);
        return value.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
      },
    },

    computed: {
      show_remove_button() {
        return this.salon_data.length > 1 ? true : false
      }
    },
    created: function () {
      evntBus.$on('open_dog_salon_dialog', (data) => {
        this.dogSalonDialog = true;
        // this.salon_data = [{}];
        this.customer = data;
        this.get_customer_pets(data);
        this.get_groomers();
      });

      
    },
  };
  </script>
  