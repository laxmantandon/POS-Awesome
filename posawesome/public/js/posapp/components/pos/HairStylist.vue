<template>
  <div v-if="show_hairstylist">
    <v-select :items="hairstylists" item-text="hairstylist_id" item-value="hairstylist_id" :label="frappe._('Hair Stylist')" dense outlined
      hide-details v-model="hairstylist" @change="get_selected_hairstylist" background-color="white"></v-select>
  </div>
</template>
  
<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    show_hairstylist: false,
    hairstylists: [],
    hairstylist: "",
  }),

  methods: {
    get_hairstylists() {
        vm = this;
        frappe.db.get_list("Neo Hair Stylist", { fields: ["name", "type", "price"] }).then((res) => {
          res.forEach(hs => {
            console.log(hs)
            p = { "hairstylist_id": hs.name, "type": hs.type, "price": hs.price }
            vm.hairstylists.push(p)
          });
        })
       evntBus.$emit('hairstylists', this.hairstylists)
    },

    // get_base_item() {
    //   vm = this;
    //   frappe.db.get_single_value("Neo Settings", "pos_item_name").then(pos_item_name => {
    //     vm.base_item = pos_item_name;
    //   });

    // },

    // get_additional_item() {
    //   vm = this;
    //   frappe.db.get_single_value("Neo Settings", "pos_additional_item_name").then(pos_add_item_name => {
    //     vm.additional_item = pos_add_item_name;
    //   });
    // },

    get_selected_hairstylist(data) {
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
      this.hairstylists = [];
      this.show_hairstylist = true;
      this.get_hairstylists(data)

    })
  },

  watch: {
    //   customer() {
    // evntBus.$emit('update_customer', this.customer);
    //   },
  },
};
</script>