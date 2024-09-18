<template>
  <el-container style="height: 100vh; border: 1px solid #eee">
    <el-aside :width="isCollapse ? '80px' : '200px'" :style="{ backgroundColor: '#00568D' }">
      <div class="profile-section">
        <div class="profile-picture">
          <img src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" alt="User" />
        </div>
        <div class="profile-name">
          <span style="color: #eee;">{{ userName }}</span>
        </div>
      </div>

      <el-button class="menu-toggle" @click="toggleMenu">
        <el-icon :size="20">
          <Menu />
        </el-icon>
      </el-button>

      <el-menu :default-active="$route.path" class="el-menu-vertical-demo" :collapse="isCollapse"
        @select="handleMenuSelect">
        <el-menu-item index="/home">
          <el-icon :size="20">
            <HomeFilled />
          </el-icon>
          <span>Inicio</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon :size="20">
            <User />
          </el-icon>
          <span>Usuarios</span>
        </el-menu-item>
        <el-menu-item index="/products">
          <el-icon :size="20">
            <Goods />
          </el-icon>
          <span>Productos</span>
        </el-menu-item>
        <el-menu-item index="/logout" @click="logout">
          <el-icon :size="20">
            <SwitchButton />
          </el-icon>
          <span>Logout</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header :style="{ backgroundColor: darkMode ? '#333' : '#B3C0D1', color: darkMode ? '#fff' : '#333' }"
        style="text-align: right; font-size: 12px; display: flex; align-items: center; padding: 0 20px;">
        <img src="../assets/img/logo.png" alt="Logo" class="logo">
        <div class="theme-switcher">
          <span :style="{ color: darkMode ? '#fff' : '#333', marginRight: '10px' }">Dark Mode</span>
          <el-switch v-model="darkMode" active-color="#409EFF" inactive-color="#C0C4CC"
            @change="toggleDarkMode"></el-switch>
        </div>
      </el-header>
      <el-main :style="{ backgroundColor: darkMode ? '#1E1E1E' : '#fff' }">
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { Goods, HomeFilled, SwitchButton, User } from '@element-plus/icons-vue';
import { mapGetters } from 'vuex';

export default {
  data() {
    return {
      isCollapse: false,
      darkMode: false,
    };
  },
  computed: {
    ...mapGetters(['userName']),
  },
  methods: {
    toggleMenu() {
      this.isCollapse = !this.isCollapse;
    },
    handleMenuSelect(key) {
      this.$router.push(key);
    },
    logout() {
      localStorage.removeItem('access_token');
      this.$store.commit('setUser', null);
      this.$router.push('/login');
    },
    toggleDarkMode(value) {
      this.darkMode = value;
    },
  },
};
</script>

<style scoped>
.el-container {
  height: 100vh;
  overflow: hidden;
}

.el-header {
  color: #333;
  line-height: 60px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  justify-content: space-between;
}

.logo {
  height: 50px;
}

.el-aside {
  transition: width 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-section {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}

.profile-picture {
  background-color: #00568D;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 10px;
}

.profile-picture img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-name {
  font-size: 14px;
}

.el-menu-vertical-demo {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.el-menu-item {
  font-size: 14px;
}

.el-menu-item .el-icon {
  font-size: 18px;
  margin-right: 10px;
}

.el-main {
  background-color: #fff;
}

.menu-toggle {
  margin: 10px;
  background-color: #00568D;
  color: white;
  border: none;
  width: 100%;
  text-align: center;
}

.menu-toggle .el-icon {
  font-size: 20px;
}

.theme-switcher {
  display: flex;
  align-items: center;
}
</style>
