<template>
  <div class="home">
    <p class="copyright">©研究生第一党支部 2024</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const isAdmin = ref(false);
const name = ref('');
const sid = ref('');
const records = ref([]);

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};


const fetchRecords = async () => {
  try {
    const user = getCookie('user');
    if (!user) {
      alert('请先登录');
      router.push('/');
      return;
    }

    const userData = JSON.parse(user);
    sid.value = userData.sid;

    const response = await fetch('/api/admin_get_records', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sid: sid.value})
    });

    if (response.ok) {
      const data = await response.json();
      records.value = data.data;
      console.log(data);
    } else {
      const errorData = await response.json();
      alert(`获取答题记录失败: ${errorData.message}`);
    }

  } catch (error) {
    console.error('获取答题记录时发生错误:', error);
    alert('获取答题记录时发生错误，请稍后重试');
  }
};


onMounted(() => {
  const user = getCookie('user');
  if (user) {
    // 注意：这种从cookie中获取权限的方法存在安全问题，不要用在正式的生产环境中
    const userData = JSON.parse(user);
    name.value = userData.name;
    sid.value = userData.sid;
    isAdmin.value = userData.role == "admin";

    if (isAdmin.value) {
      fetchRecords();
    }
  }
});
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}



.copyright {
  position: fixed;
  bottom: 0;
  font-size: 1rem;
  color: #666;
  margin-top: 2rem;
}

</style>