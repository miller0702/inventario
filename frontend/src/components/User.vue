<template>
  <div>
    <h2>Lista de Usuarios</h2>
    <div class="header-actions">
      <el-button @click="openSaveModal" type="primary">Agregar Usuario</el-button>
      <el-input v-model="search" style="width: 200px" placeholder="Buscar usuario" :suffix-icon="Search" />
    </div>

    <!-- Tabla Listar Usuarios -->
    <el-table :data="filteredUsers" stripe style="width: 100%">
      <el-table-column prop="id" label="#" width="100"></el-table-column>
      <el-table-column prop="nombre" label="Nombre" width="180"></el-table-column>
      <el-table-column prop="apellido" label="Apellido" width="180"></el-table-column>
      <el-table-column prop="documento" label="Documento" width="180"></el-table-column>
      <el-table-column prop="email" label="Email"></el-table-column>
      <el-table-column label="Acciones" width="180">
        <template v-slot:default="{ row }">
          <el-button @click="openEditModal(row)" type="primary">
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
      :page-size="pageSize" :total="totalUsers" layout="total, prev, pager, next, jumper, sizes">
    </el-pagination>

    <!-- Modal de Agregar Usuario -->
    <el-dialog title="Agregar Nuevo Usuario" v-model="isSaveModalVisible" width="30%" :before-close="handleClose">
      <el-form :model="user" ref="form">
        <el-form-item label="Nombre">
          <el-input v-model="user.nombre"></el-input>
        </el-form-item>
        <el-form-item label="Apellido">
          <el-input v-model="user.apellido"></el-input>
        </el-form-item>
        <el-form-item label="Documento">
          <el-input v-model="user.documento"></el-input>
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="user.email"></el-input>
        </el-form-item>
        <el-form-item label="Contraseña">
          <el-input v-model="user.contrasena" type="password" show-password></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="saveUser">Guardar</el-button>
      </template>
    </el-dialog>

    <!-- Modal de Editar Usuario -->
    <el-dialog title="Editar Usuario" v-model="isEditModalVisible" width="30%" @close="handleCloseEdit">
      <el-form :model="currentUser" ref="formEdit">
        <el-form-item label="Nombre">
          <el-input v-model="currentUser.nombre"></el-input>
        </el-form-item>
        <el-form-item label="Apellido">
          <el-input v-model="currentUser.apellido"></el-input>
        </el-form-item>
        <el-form-item label="Documento">
          <el-input v-model="currentUser.documento"></el-input>
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="currentUser.email"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleCloseEdit">Cancelar</el-button>
        <el-button type="primary" @click="saveChanges">Guardar</el-button>
      </template>
    </el-dialog>

    <!-- Modal de Confirmar Eliminación -->
    <el-dialog title="Confirmar Eliminación" v-model="isDeleteModalVisible" width="30%" @close="handleCloseDelete">
      <p>¿Está seguro de que desea eliminar el usuario?</p>
      <template #footer>
        <el-button @click="handleCloseDelete">Cancelar</el-button>
        <el-button type="danger" @click="confirmDelete">Eliminar</el-button>
      </template>
    </el-dialog>
  </div>

  <el-alert v-if="alertMessage" :title="alertMessage" :type="alertType" />
</template>

<script>
import axios from '../services/api';
import { Delete, EditPen, Search } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';

export default {
  data() {
    return {
      users: [],
      search: '',
      currentPage: 1,
      pageSize: 10,
      totalUsers: 0,
      isSaveModalVisible: false,
      isEditModalVisible: false,
      isDeleteModalVisible: false,
      user: {
        nombre: '',
        apellido: '',
        documento: '',
        email: '',
        contrasena: ''
      },
      currentUser: null,
      userIdToDelete: null,
      alertMessage: '',
      alertType: ''
    };
  },
  components: {
    Delete,
    EditPen,
    Search
  },
  computed: {
    filteredUsers() {
      const searchLower = this.search.toLowerCase();
      return this.users.filter(user =>
        user.nombre.toLowerCase().includes(searchLower) ||
        user.apellido.toLowerCase().includes(searchLower) ||
        user.documento.toLowerCase().includes(searchLower) ||
        user.email.toLowerCase().includes(searchLower)
      );
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/users/getUsers/');
        this.users = response.data;
        this.totalUsers = this.users.length;
      } catch (error) {
        ElMessage.error('Error al obtener usuarios: ' + error.message);
      }
    },
    async handleSizeChange(size) {
      this.pageSize = size;
      await this.fetchUsers();
    },
    async handleCurrentChange(page) {
      this.currentPage = page;
      await this.fetchUsers();
    },
    openSaveModal() {
      this.isSaveModalVisible = true;
    },
    async openEditModal(user) {
      this.currentUser = { ...user };
      this.isEditModalVisible = true;
    },
    openDeleteModal(userId) {
      this.userIdToDelete = userId;
      this.isDeleteModalVisible = true;
    },
    handleClose(done) {
      done();
      this.resetForm();
    },
    handleCloseEdit() {
      this.isEditModalVisible = false;
    },
    handleCloseDelete() {
      this.isDeleteModalVisible = false;
    },
    resetForm() {
      this.user = {
        nombre: '',
        apellido: '',
        documento: '',
        email: '',
        contrasena: ''
      };
    },
    async saveUser() {
      try {
        await axios.post('/users/registerUser/', this.user, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        ElMessage.success('Usuario guardado exitosamente');
        this.isSaveModalVisible = false;
        this.resetForm();
        await this.fetchUsers();
      } catch (error) {
        ElMessage.error('Error al guardar el usuario: ' + error.message);
      }
    },
    async saveChanges() {
      try {
        const updatedUser = { ...this.currentUser };
        if (!updatedUser.contrasena) {
          delete updatedUser.contrasena;
        }

        await axios.put(`/users/updateUser/${this.currentUser.id}`, updatedUser, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json'
          }
        });

        this.handleCloseEdit();
        ElMessage.success('Usuario actualizado exitosamente');
        await this.fetchUsers();
      } catch (error) {
        ElMessage.error('Error al actualizar el usuario: ' + error.message);
      }
    },
    async confirmDelete() {
      if (this.userIdToDelete == null || isNaN(this.userIdToDelete)) {
        ElMessage.error('ID de usuario inválido: ' + this.userIdToDelete);
        return;
      }

      try {
        await axios.delete(`/users/deleteUser/${this.userIdToDelete}`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        this.handleCloseDelete();
        ElMessage.success('Usuario eliminado exitosamente');
        await this.fetchUsers();
      } catch (error) {
        ElMessage.error('Error al eliminar el usuario: ' + error.message);
      }
    }
  },
  created() {
    this.fetchUsers();
  }
};
</script>

<style>
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  gap: 20px;
}

.header-actions .el-input {
  flex: 1;
  margin-right: 10px;
}

.header-actions .el-button {
  flex-shrink: 0;
}
</style>
