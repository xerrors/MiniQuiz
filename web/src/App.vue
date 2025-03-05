<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

// 根据路由判断是否是首页
const router = useRouter();
console.log(router.currentRoute.value)
const isHome = computed(() => router.currentRoute.value.meta.isHome);

const goHome = () => {
  router.push('/');
};

const goBack = () => {
  router.back();
};

const logout = () => {
  document.cookie = 'user=; path=/';
  location.reload();
  router.push('/');
};
</script>

<template>
  <div v-if="isHome" class="bar">
    <p @click="logout"><img src="/logo.png" alt=""><span class="title-text">AIGC科普答题平台</span></p>
  </div>
  <div v-else class="bar">
    <button @click="goBack" class="nav-btn"> <img src="/icons/返回.svg" alt=""></button>
    <p><img src="/logo.png" alt=""><span class="title-text">AIGC科普答题平台</span></p>
    <button @click="goHome" class="nav-btn"><img src="/icons/首页-置灰.svg" alt=""></button>
  </div>
  <div class="router-view">
    <RouterView />
  </div>
</template>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
}

.bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 4.5em;
  background: linear-gradient(to right, #2563EB, #3B82F6);
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 10px rgba(37, 99, 235, 0.3);
}

.bar > p {
  width: 100%;
  text-align: center;
  color: white;
  font-size: 1.3rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  padding: 0;
  margin: 0;
}

.title-text {
  background: linear-gradient(to right, #FBBF24, #FEF3C7);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 1px 3px rgba(251, 191, 36, 0.3);
  letter-spacing: 0.5px;
}

.bar > p > img {
  border-radius: 8px;
  height: 2.2rem;
  width: 2.2rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
  border: 2px solid rgba(255, 255, 255, 0.7);
  transition: transform 0.2s ease;
}

.bar > p:active > img {
  transform: scale(0.95);
}

.nav-btn {
  background-color: rgba(255, 255, 255, 0.15);
  color: white;
  font-size: 1em;
  border: none;
  padding: 0.6em;
  cursor: pointer;
  margin: 0 1em;
  border-radius: 50%;
  transition: all 0.2s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2.5em;
  height: 2.5em;
}

.nav-btn:hover {
  background-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
}

.nav-btn:active {
  background-color: rgba(255, 255, 255, 0.3);
  transform: translateY(0);
}

.bar > button > img {
  width: 1.4em;
  height: 1.4em;
  filter: brightness(1.2);
}

.router-view {
  width: 100%;
  height: calc(100vh - 4.5em);
  overflow: auto;
  padding-bottom: 4em;
  box-sizing: border-box;
  background-color: #F5F8FF;
}

@media (prefers-reduced-motion: no-preference) {
  .nav-btn {
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  .nav-btn:hover {
    transform: translateY(-3px);
  }

  .router-view {
    scroll-behavior: smooth;
  }
}
</style>
