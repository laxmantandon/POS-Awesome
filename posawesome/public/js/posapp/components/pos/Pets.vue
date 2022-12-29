<template>
  <div v-if="show_pets">
    <v-select :items="customer_pets" item-text="pet_name" item-value="pet_id" :label="frappe._('Customer Pets')" dense outlined
      hide-details v-model="pets" multiple @change="get_selected_pets" background-color="white"></v-select>
  </div>
</template>
  
<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    show_pets: false,
    customer_pets: [],
    base_item: "",
    additional_item: "",
  }),

  methods: {
    get_customer_pets(selected_customer) {
      if (selected_customer == null) {
        this.customer_pets = [];
        this.pets = [];
      } else {
        this.customer_pets = [];
        this.pets = [];
        vm = this;
        frappe.db.get_list("Pet", { fields: ["name", "pet_name"], filters: { customer: selected_customer } }).then((res) => {
          res.forEach(pet => {
            console.log(pet)
            p = { "pet_id": pet.name, "pet_name": pet.pet_name }
            this.customer_pets.push(p)
          })
        }).catch(e => {
          console.log('Error', e)
        })

      }
      evntBus.$emit('customer_pets', this.customer_pets)
    },

    get_base_item() {
      vm = this;
      frappe.db.get_single_value("Neo Settings", "pos_item_name").then(pos_item_name => {
        vm.base_item = pos_item_name;
      });

    },

    get_additional_item() {
      vm = this;
      frappe.db.get_single_value("Neo Settings", "pos_additional_item_name").then(pos_add_item_name => {
        vm.additional_item = pos_add_item_name;
      });
    },

    get_selected_pets(data) {
      console.log(data)
      if (data.length > 2) {
        evntBus.$emit("clear_items")
        vm = this;

        frappe.db.get_doc("Item", vm.base_item).then(d => {
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

        frappe.db.get_doc("Item", vm.additional_item).then(e => {
          // console.log(e)
          let item2 = {
            item_code: e.item_code,
            item_name: e.item_name,
            qty: vm.pets.length - 2,
            uom: e.stock_uom,
            stock_uom: e.stock_uom
          }
          evntBus.$emit('add_item', item2);
        });

        // evntBus.$emit('add_item', item1);
        // evntBus.$emit('add_item', item2);

      } else {
        evntBus.$emit("clear_items")
        frappe.db.get_doc("Item", vm.base_item).then(d => {
          // console.log(d)
          let item1 = {
            item_code: d.item_code,
            item_name: d.item_name,
            qty: 1,
            uom: d.stock_uom,
            stock_uom: d.stock_uom
          }
          evntBus.$emit('add_item', item1);
        })

      }
    }


  },

  computed: {},

  created: function () {
    this.$nextTick(function () { });
    evntBus.$on('update_customer', (data) => {
      this.customer_pets = [];
      this.pets = [];
      this.show_pets = true;
      this.get_base_item();
      this.get_additional_item();
      this.get_customer_pets(data)

    })
  },

  watch: {
    //   customer() {
    // evntBus.$emit('update_customer', this.customer);
    //   },
  },
};
</script>