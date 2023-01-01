<template>
  <v-row justify="center">
    <v-dialog v-model="petDialog" max-width="600px" persistent>
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{ __('New pet') }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Pet Name')"
                  background-color="white"
                  hide-details
                  v-model="pet_name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Pet Breed')"
                  v-model="primary_breed"
                  :items="primary_breeds"
                  background-color="white"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Pet Type')"
                  v-model="pet_type"
                  :items="['Dog', 'Cat']"
                  background-color="white"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Color')"
                  background-color="white"
                  hide-details
                  v-model="color"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Gender')"
                  v-model="gender"
                  :items="['Male', 'Female']"
                  background-color="white"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-menu
                  ref="birthday_menu"
                  v-model="birthday_menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  dense
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="date_of_birth"
                      :label="frappe._('Birthday')"
                      readonly
                      dense
                      clearable
                      hide-details
                      v-bind="attrs"
                      v-on="on"
                      color="primary"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="date_of_birth"
                    color="primary"
                    no-title
                    scrollable
                    :max="frappe.datetime.now_date()"
                    @input="birthday_menu = false"
                  >
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Weight in Kgs')"
                  v-model="weight_in_kgs"
                  :items="['< 10 KG', '10-20 KG', '20-30 KG', '> 30 KG']"
                  background-color="white"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">{{
            __('Close')
          }}</v-btn>
          <v-btn color="success" dark @click="submit_dialog">{{
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
    petDialog: false,
    pet_name: "",
    primary_breed: "",
    primary_breeds: [],
    pet_type: "",
    color: "",
    colors: [],
    gender: "",
    date_of_birth: "",
    birthday_menu: false,
    weight_in_kgs: "",
    pos_profile: '',
    customer: ''
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.petDialog = false;
    },
    getPetBreed() {
      if (this.primary_breeds.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Pet Breed', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.primary_breeds.push(el.name);
            });
          }
        });
    },

    submit_dialog() {
      if (this.pet_name) {
        const vm = this;
        const args = {
          pet_name: this.pet_name,
          // company: this.pos_profile.company,
          primary_breed: this.primary_breed,
          pet_type: this.pet_type,
          color: this.color,
          gender: this.gender,
          date_of_birth: this.date_of_birth,
          weight_in_kgs: this.weight_in_kgs,
          customer: this.customer
        };
        frappe.call({
          method: 'posawesome.posawesome.api.neoapi.create_pet',
          args: args,
          callback: (r) => {
            if (!r.exc && r.message.name) {
              evntBus.$emit('show_mesage', {
                text: __('Pet created successfully.'),
                color: 'success',
              });
              args.name = r.message.name;
              frappe.utils.play_sound('submit');
              evntBus.$emit('reload_pets', vm.customer);
              vm.pet_name = '';
              vm.primary_breed = '';
              vm.pet_type = '';
              vm.color = '';
              vm.gender = '';
              vm.weight_in_kgs = '';
              vm.date_of_birth = '';
              // vm.customer = '';
              vm.petDialog = false;
            }
          },
        });
        this.petDialog = false;
      }
    },
  },
  created: function () {

    evntBus.$on("update_customer", data => {
      this.customer = data;
    })
    evntBus.$on('open_new_pet', () => {
      this.petDialog = true;
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getPetBreed();
  },
};
</script>
