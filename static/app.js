new Vue({
 el: '#orders-app',
 data: {
  orders:[]
 },
 created() {
   const vm = this;
   axios.get('/api/orders/?format=json').then(function(responce){
    //console.log(responce.data);
    vm.orders = responce.data
   });
 }
})