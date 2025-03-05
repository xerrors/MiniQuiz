<template>
  <div class="records">
    <h1>答题记录</h1>
    <div v-if="records.length === 0">
      <p>还没有答题记录</p>
      <button @click="startQuiz">开始答题</button>
    </div>
    <div v-else class="record-list">
      <div class="card" v-for="record in records" :key="record.id" @click="viewRecord(record)">
        <div class="card-content">
          <p><strong>{{ formatDate(record.date) }}</strong></p>
          <p><strong>分数: </strong>{{ record.score }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const records = ref([]);
const sid = ref(null);

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

const formatDate = (isoString) => {
  const date = new Date(isoString);

  const year = date.getFullYear();
  const month = date.getMonth() + 1; // getMonth() 返回的月份从0开始，需要加1
  const day = date.getDate();
  const hours = date.getHours();
  const minutes = date.getMinutes();

  const formattedDate = `${year}年${month}月${day}日 ${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
  return formattedDate;
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

    const response = await fetch('http://127.0.0.1:5000/get_records', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sid: sid.value })
    });

    if (response.ok) {
      const data = await response.json();
      records.value = data.data;
      records.value.reverse();
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

const startQuiz = () => {
  router.push('/quiz');
};

const viewRecord = (record) => {
  router.push({
    name: 'Result',
    query: {
      isHistory: true,
      date: record.date,
      score: record.score,
      questions: record.questions,
      answers: record.answers
    }
  });
};

onMounted(() => {
  fetchRecords();
});
</script>

<style scoped>
.records {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: calc(100vh - 8em);
  text-align: center;
  width: 100%;
  box-sizing: border-box;
  padding: 0.5rem;
}

h1 {
  font-size: 2rem;
  color: #555;
  margin-bottom: 2rem;
}

button {
  font-size: 1.2rem;
  padding: 0.8rem 1.6rem;
  background-color: #C5262D;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #a60030;
}

.record-list {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 600px;
  box-sizing: border-box;
}

.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
  margin: 0.85rem 1rem;
  padding: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-sizing: border-box;
  background-color: #F8FAFF;
  border: 1px solid #E6EEFF;
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 4px;
  background: linear-gradient(to bottom, #3B82F6, #93C5FD);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.15);
  border-color: #3B82F6;
}

.card-content {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
  padding-left: 12px;
}

.card-content p {
  margin: 0.5rem 0;
}

.card-content p:first-child {
  color: #4B5563;
  font-size: 0.95rem;
}

.card-content p:last-child {
  background-color: #3B82F6;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 20px;
  font-size: 0.9rem;
}
</style>
