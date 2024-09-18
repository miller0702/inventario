<template>
  <div class="login-container">
    <el-card class="login-card" shadow="always">
      <div class="login-icon">
        <i class="el-icon-user"></i>
      </div>
      <img src="../assets/img/logo.png" alt="Logo" class="logo">
      <h2 class="login-title">Login</h2>
      <el-form :model="form" @submit.native.prevent="login" class="login-form">
        <el-form-item>
          <el-input v-model="form.email" type="email" placeholder="Email" />
        </el-form-item>
        <el-form-item>
          <el-input
            v-model="form.contrasena"
            type="password"
            placeholder="Contraseña"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit">Login</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import axios from '../services/api';

export default {
  data() {
    return {
      form: {
        email: '',
        contrasena: '',
      },
      formLabelWidth: '100px',
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/users/login/', {
          email: this.form.email,
          contrasena: this.form.contrasena,
        });
        const { access_token } = response.data;

        this.$store.dispatch('login', { email: this.form.email, token: access_token });

        this.$router.push('/home');
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Error al iniciar sesión. Inténtalo de nuevo más tarde.';
        this.$message.error(errorMessage);
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  width: 400px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.login-icon {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  font-size: 50px;
  color: #409eff;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.login-form .el-form-item {
  margin-bottom: 15px;
}

.el-form-item__label {
  font-size: 14px;
  color: #666;
}

.el-button {
  width: 100%;
}

.logo {
  height: 15vh;
}
</style>
