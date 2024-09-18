<template>
  <div>
    <h2>Lista de Productos</h2>
    <div class="header-actions">
      <el-button @click="openSaveModal" type="primary">Agregar Producto</el-button>
      <el-input v-model="search" style="width: 200px" placeholder="Buscar producto" :suffix-icon="Search" />
    </div>

    <!-- Tabla Listar Productos -->
    <el-table :data="filteredProducts" stripe style="width: 100%">
      <el-table-column prop="id" label="#" width="100"></el-table-column>
      <el-table-column prop="nombre" label="Nombre" width="180"></el-table-column>
      <el-table-column prop="precio" label="Precio" width="180"></el-table-column>
      <el-table-column prop="cantidad" label="Cantidad" width="180"></el-table-column>
      <el-table-column prop="descripcion" label="Descripción"></el-table-column>
      <el-table-column label="Acciones">
        <template v-slot:default="{ row }">
          <el-button @click="openViewModal(row.id)" type="primary">
            <el-icon :size="20">
              <View />
            </el-icon>
          </el-button>
          <el-button @click="openEditModal(row)" type="warning">
            <el-icon :size="20">
              <EditPen />
            </el-icon>
          </el-button>
          <el-button @click="openDeleteModal(row.id)" type="danger">
            <el-icon :size="20">
              <Delete />
            </el-icon>
          </el-button>
        </template>
      </el-table-column>
    </el-table><br>

    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
      :page-size="pageSize" :total="totalProducts" layout="total, prev, pager, next, jumper, sizes">
    </el-pagination>

    <!-- Modal de Agregar Producto -->
    <el-dialog title="Agregar Nuevo Producto" v-model="isSaveModalVisible" width="30%" :before-close="handleClose">
      <el-form :model="product" ref="form">
        <el-form-item label="Nombre">
          <el-input v-model="product.nombre"></el-input>
        </el-form-item>
        <el-form-item label="Precio">
          <el-input v-model="product.precio" type="number"></el-input>
        </el-form-item>
        <el-form-item label="Cantidad">
          <el-input v-model="product.cantidad" type="number"></el-input>
        </el-form-item>
        <el-form-item label="Descripción">
          <el-input v-model="product.descripcion"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="saveProduct">Guardar</el-button>
      </template>
    </el-dialog>

    <!-- Modal de Visualización de Producto -->
    <el-dialog title="Detalles del Producto" v-model="isViewModalVisible" width="50%">
      <div v-if="viewProduct">
        <el-form :model="viewProduct" label-width="120px">
          <el-form-item label="Nombre">
            <el-input v-model="viewProduct.nombre" disabled></el-input>
          </el-form-item>
          <el-form-item label="Precio">
            <el-input v-model="viewProduct.precio" disabled></el-input>
          </el-form-item>
          <el-form-item label="Cantidad">
            <el-input v-model="viewProduct.cantidad" disabled></el-input>
          </el-form-item>
          <el-form-item label="Descripción">
            <el-input v-model="viewProduct.descripcion" disabled></el-input>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <el-button @click="handleCloseView">Cerrar</el-button>
      </template>
    </el-dialog>

    <!-- Modal de Editar Producto -->
    <el-dialog title="Editar Producto" v-model="isEditModalVisible" width="30%" @close="handleCloseEdit">
      <el-form :model="currentProduct" ref="formEdit">
        <el-form-item label="Nombre">
          <el-input v-model="currentProduct.nombre"></el-input>
        </el-form-item>
        <el-form-item label="Precio">
          <el-input v-model="currentProduct.precio" type="number"></el-input>
        </el-form-item>
        <el-form-item label="Cantidad">
          <el-input v-model="currentProduct.cantidad" type="number"></el-input>
        </el-form-item>
        <el-form-item label="Descripción">
          <el-input v-model="currentProduct.descripcion"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCloseEdit">Cancelar</el-button>
        <el-button type="primary" @click="saveChanges">Guardar</el-button>
      </template>
    </el-dialog>

    <!-- Modal de Confirmar Eliminación -->
    <el-dialog title="Confirmar Eliminación" v-model="isDeleteModalVisible" width="30%" @close="handleCloseDelete">
      <p>¿Está seguro de que desea eliminar el producto?</p>
      <template #footer>
        <el-button @click="handleCloseDelete">Cancelar</el-button>
        <el-button type="danger" @click="confirmDelete">Eliminar</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script>
import axios from '../services/api';
import { DeleteFilled, EditPen, Search, View } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      products: [],
      search: '',
      currentPage: 1,
      pageSize: 10,
      totalProducts: 0,
      isSaveModalVisible: false,
      isViewModalVisible: false,
      isEditModalVisible: false,
      isDeleteModalVisible: false,
      product: {
        nombre: '',
        precio: 0,
        cantidad: 0,
        descripcion: ''
      },
      currentProduct: null,
      productIdToDelete: null,
      viewProduct: null,
    };
  },
  components: {
    DeleteFilled,
    EditPen,
    Search,
    View
  },
  computed: {
    filteredProducts() {
      const searchLower = this.search.toLowerCase();
      return this.products.filter(product =>
        product.nombre.toLowerCase().includes(searchLower) ||
        product.descripcion.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('/products/getProducts/');
        this.products = response.data;
        this.totalProducts = this.products.length;
      } catch (error) {
        ElMessage.error('Error al obtener productos:', error);
      }
    },
    async handleSizeChange(size) {
      this.pageSize = size;
      await this.fetchProducts();
    },
    async handleCurrentChange(page) {
      this.currentPage = page;
      await this.fetchProducts();
    },
    openSaveModal() {
      this.isSaveModalVisible = true;
    },
    async openEditModal(product) {
      this.currentProduct = { ...product };
      this.isEditModalVisible = true;
    },
    openDeleteModal(productId) {
      this.productIdToDelete = productId;
      this.isDeleteModalVisible = true;
    },
    async openViewModal(productId) {
      try {
        const response = await axios.get(`/products/getProduct/${productId}`);
        this.viewProduct = response.data;
        this.isViewModalVisible = true;
      } catch (error) {
        ElMessage.error('Error al obtener los detalles del producto: ' + error.message);
      }
    },
    handleClose(done) {
      done();
      this.resetForm();
    },
    handleCloseView() {
      this.isViewModalVisible = false;
    },
    handleCloseEdit() {
      this.isEditModalVisible = false;
    },
    handleCloseDelete() {
      this.isDeleteModalVisible = false;
    },
    resetForm() {
      this.product = {
        nombre: '',
        precio: 0,
        cantidad: 0,
        descripcion: ''
      };
    },
    async saveProduct() {
      try {
        await axios.post('/products/registerProduct/', this.product, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        ElMessage.success('Producto guardado con éxito.');
        this.isSaveModalVisible = false;
        this.resetForm();
        await this.fetchProducts();
      } catch (error) {
        ElMessage.error('Error al guardar el producto: ' + error.message);
      }
    },
    async saveChanges() {
      try {
        await axios.put(`/products/updateProduct/${this.currentProduct.id}`, this.currentProduct, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });
        ElMessage.success('Producto actualizado con éxito.');
        this.handleCloseEdit();
        await this.fetchProducts();
      } catch (error) {
        ElMessage.error('Error al actualizar el producto: ' + error.message);
      }
    },
    async confirmDelete() {
      try {
        await axios.delete(`/products/deleteProduct/${this.productIdToDelete}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        ElMessage.success('Producto eliminado con éxito.');
        this.handleCloseDelete();
        await this.fetchProducts();
      } catch (error) {
        ElMessage.error('Error al eliminar el producto: ' + error.message);
      }
    }
  },
  created() {
    this.fetchProducts();
  }
};
</script>

<style scoped>
.header-actions {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
