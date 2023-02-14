<template>
  <v-row>
    <v-col>
      <div>
        <v-autocomplete dense clearable auto-select-first outlined color="primary" :label="frappe._('Customer')"
          v-model="customer" :items="customers" item-text="customer_name" item-value="name" background-color="white"
          :no-data-text="__('Customer not found')" hide-details :filter="customFilter" :disabled="readonly"
          append-icon="mdi-plus" @click:append="new_customer" prepend-inner-icon="mdi-account-edit"
          @click:prepend-inner="edit_customer">
          <template v-slot:item="data">
            <template>
              <v-list-item-content>
                <v-list-item-title class="primary--text subtitle-1"
                  v-html="data.item.customer_name"></v-list-item-title>
                <v-list-item-subtitle v-if="data.item.customer_name != data.item.name"
                  v-html="`ID: ${data.item.name}`"></v-list-item-subtitle>
                <v-list-item-subtitle v-if="data.item.neo_membership_number"
                  v-html="`MEMBERSHIP NO : ${data.item.neo_membership_number}`"></v-list-item-subtitle>
                <v-list-item-subtitle v-if="data.item.tax_id"
                  v-html="`TAX ID: ${data.item.tax_id}`"></v-list-item-subtitle>
                <v-list-item-subtitle v-if="data.item.email_id"
                  v-html="`Email: ${data.item.email_id}`"></v-list-item-subtitle>
                <v-list-item-subtitle v-if="data.item.mobile_no"
                  v-html="`Mobile No: ${data.item.mobile_no}`"></v-list-item-subtitle>
                <v-list-item-subtitle v-if="data.item.primary_address"
                  v-html="`Primary Address: ${data.item.primary_address}`"></v-list-item-subtitle>
              </v-list-item-content>
            </template>
          </template>
        </v-autocomplete>

      </div>
    </v-col>
    <v-col cols="1" v-if="pos_profile.pos_profile.neo_is_dog_salon == 1 && customer">
      <v-btn @click="show_dog_salon_dialog()" icon color="primary">
        <v-icon>mdi-dog-side</v-icon>
      </v-btn>
    </v-col>
  </v-row>

</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
  }),

  methods: {
    get_customer_names() {
      const vm = this;
      if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            console.info('loadCustomers');
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit('open_new_customer');
    },
    edit_customer() {
      evntBus.$emit('open_edit_customer');
    },
    customFilter(item, queryText, itemText) {
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const textSixth = item.neo_membership_number ? item.neo_membership_number.toLowerCase(): '';
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1 ||
        textSixth.indexOf(searchText) > -1
      );
    },

    show_dog_salon_dialog() {
      if (this.pos_profile.pos_profile.neo_is_dog_salon == 1 && (this.customer != undefined || this.customer == '')) {
        evntBus.$emit('open_dog_salon_dialog', this.customer)
      }
    }
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
        if (this.pos_profile.pos_profile.neo_is_dog_salon == 1 && (customer != undefined || customer == '')) {
          evntBus.$emit('open_dog_salon_dialog', customer)
        }
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
    });
  },

  watch: {
    customer() {
      evntBus.$emit('update_customer', this.customer);
    },
  },
};
</script>