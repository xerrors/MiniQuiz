<template>
  <div class="home">
    <img src="/logo.png" alt="logo" />
    <p class="xueyuan">江南语析科技有限公司</p>
    <template v-if="!isLoggedIn">
      <h1>AIGC科普答题平台</h1>
      <form @submit.prevent="login">
        <input v-model="sid" type="text" placeholder="学号" required />
        <input v-model="password" type="password" placeholder="密码（默认是学号）" required />
        <button type="submit">登录</button>
      </form>
    </template>
    <template v-else>
      <h1>你好，{{ name }}</h1>
      <div class="buttons">
        <button @click="startQuiz">开始答题 <img src="/icons/签署协议.svg" alt=""></button>
        <button @click="viewQuizHistory">答题记录 <img src="/icons/分享.svg" alt=""></button>
        <button v-if="role === 'admin'" @click="goToAdmin" class="admin-btn">管理员界面 <img src="/icons/管理员.svg" alt=""></button>
        <!-- <button v-if="role=='admin'" @click="checkAll">查看汇总 <img src="/icons/签署协议.svg" alt=""></button> -->
      </div>
    </template>
    <p class="copyright">开发 © 江南语析科技有限公司 2024</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isLoggedIn = ref(false);
const name = ref('');
const sid = ref('');
const password = ref('');
const role = ref('');

onMounted(() => {
  const user = getCookie('user');
  if (user) {
    // 注意：这种从cookie中获取权限的方法存在安全问题，不要用在正式的生产环境中
    const userData = JSON.parse(user);
    name.value = userData.name;
    sid.value = userData.sid;
    role.value = userData.role;
    isLoggedIn.value = true;
  }
});

const login = async () => {
  const response = await fetch('http://127.0.0.1:5000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ sid: sid.value, password: password.value })
  });

  if (response.ok) {
    const data = await response.json();
    document.cookie = `user=${JSON.stringify(data)}; path=/`;
    name.value = data.name;
    role.value = data.role;
    isLoggedIn.value = true;
  } else {
    alert('登录失败，请检查用户名和密码');
  }
};

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

const startQuiz = () => {
  router.push('/quiz');
};

const viewQuizHistory = async () => {
  router.push('/records');
};

const checkAll = async () => {
  router.push('/overall');
};

const goToAdmin = () => {
  router.push('/admin');
};
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  width: 100%;
  min-width: calc(100vw - 4em);
}

.home > img {
  margin-top: 10vh;
  width: auto;
  height: 80px;
  margin-bottom: 2rem;
}

.xueyuan {
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: 10vh;
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  /* margin-top: 10vh; */
}

button > img {
  width: 1.2rem;
  height: 1.2rem;
  margin-left: 0.5rem;
  position: relative;
  top: 0.2rem;
}

h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 2rem;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

input {
  font-size: 1.2rem;
  padding: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

button {
  font-size: 1.2rem;
  padding: 0.8rem 2rem;
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 1rem;
}

button:hover {
  background-color: #2563EB;
}

button[type="submit"] {
  width: 100%;
}

.admin-btn {
  background-color: #10B981;
}

.admin-btn:hover {
  background-color: #059669;
}

.copyright {
  position: fixed;
  bottom: 0;
  font-size: 1rem;
  color: #666;
  margin-top: 2rem;
}
</style>
