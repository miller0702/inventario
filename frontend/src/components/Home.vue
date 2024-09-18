<template>
  <div class="home-container">
    <el-row :gutter="20">
      <!-- Card de Usuarios -->
      <el-col :span="12">
        <el-card class="card">
          <el-row class="card-row">
            <el-icon :size="100" style="color: #00568D;">
              <User />
            </el-icon>
            <div class="card-body">
              <span>Usuarios Registrados</span>
              <p>{{ totalUsuarios }} Usuarios</p>
            </div>
          </el-row>
        </el-card>
      </el-col>
      <!-- Card de Productos -->
      <el-col :span="12">
        <el-card class="card">
          <el-row class="card-row">
            <el-icon :size="100" style="color: #00568D;">
              <ShoppingCart />
            </el-icon>
            <div class="card-body">
              <span>Productos Registrados</span>
              <p>{{ totalProductos }} Productos</p>
            </div>
          </el-row>
        </el-card>
      </el-col>      
    </el-row>
  </div>
</template>

<script>
import axios from '../services/api';
import { User, ShoppingCart } from '@element-plus/icons-vue';

export default {
  data() {
    return {
      totalUsuarios: 0,
      totalProductos: 0
    };
  },
  components: {
    User,
    ShoppingCart
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const usersResponse = await axios.get('/users/count/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        this.totalUsuarios = usersResponse.data;

        const productsResponse = await axios.get('/products/count/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        this.totalProductos = productsResponse.data;
      } catch (error) {
        console.error('Error al obtener datos:', error);
        this.$message.error('Error al cargar los datos');
      }
    }
  }
};
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.card-row {
  text-align: center;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.card-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-body p {
  font-size: 30px;
  margin-top: 10px;
}

span{
  font-size: 25px;
  font-weight: 600;
}
</style>