<template>
  <div class="quiz-view">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>正在加载题目...</p>
    </div>
    <div v-else-if="questions.length === 0" class="error-message">
      <p>无法加载题目，请检查网络连接后刷新页面</p>
      <button class="btn" @click="fetchRandomQuestions">重试</button>
    </div>
    <div v-else class="question">
      <h2 class="q-count"><span>{{ (currentQuestionIndex+1) }}</span> / {{ questions.length }}</h2>
      <p class="q-text">{{ questions[currentQuestionIndex].题目 }}</p>
      <div class="options">
        <div v-for="(option, name) in optionsLabel" :key="name" class="option" :class="{ checked: isChecked(name) }">
          <label class="radio-label">
            <input type="radio"
                  :value="name" v-model="answers[currentQuestionIndex]"/>
            {{ name + ". " + option }}
          </label>
        </div>
      </div>
      <div class="buttons">
        <button v-if="currentQuestionIndex < questions.length-1" class="btn btn-next" @click="submitAnswer" :disabled="!answers[currentQuestionIndex]">下一题</button>
        <button v-else @click="submitQuiz" class="btn btn-final"  :disabled="!answers[currentQuestionIndex]">提交答卷</button>
        <button v-if="currentQuestionIndex > 0" class="btn btn-pre" @click="handlePrev">上一题</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const QLEN = 20;
const questions = ref([]);
const currentQuestionIndex = ref(0);
const answers = ref([]);
const loading = ref(true);

const getCookie = (name) => {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
};

const fetchRandomQuestions = async () => {
  loading.value = true;
  try {
    const response = await fetch('/api/get_random_questions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ count: QLEN })
    });

    if (response.ok) {
      const data = await response.json();
      questions.value = data.questions;
      answers.value = Array(questions.value.length).fill(null);
    } else {
      alert('获取题目失败，请刷新页面重试');
    }
  } catch (error) {
    console.error('获取题目时出错:', error);
    alert('获取题目失败，请检查网络连接');
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchRandomQuestions();
});

const handlePrev = () => {
  currentQuestionIndex.value--;
};

const isChecked = (name) => answers.value[currentQuestionIndex.value] === name;

const optionsLabel = computed(() => {
  if (questions.value.length === 0 || !questions.value[currentQuestionIndex.value]) {
    return { A: '', B: '', C: '', D: '' };
  }
  return {
    A: questions.value[currentQuestionIndex.value].A,
    B: questions.value[currentQuestionIndex.value].B,
    C: questions.value[currentQuestionIndex.value].C,
    D: questions.value[currentQuestionIndex.value].D,
  };
});

const submitAnswer = () => {;
  currentQuestionIndex.value++;
};

const submitQuiz = async () => {
  const query = {
    answers: JSON.stringify(answers.value),
    questions: JSON.stringify(questions.value),
    score: `${answers.value.filter((answer, index) => answer === questions.value[index].答案).length} / ${QLEN}`,
    date: new Date().toISOString()
  };
  const user = getCookie('user');
  if (user) {
    const userData = JSON.parse(user);
    query.sid = userData.sid;
    query.name = userData.name;
  } else {
    alert('请先登录');
    router.push('/');
  }
  // 将 query 保存到服务器，以便后续查看答题记录。
  try {
    const response = await fetch('/api/save_records', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(query)
    });

    if (response.ok) {
      router.push({
        name: 'Result',
        query: query
      });
    } else {
      const errorData = await response.json();
      alert(`提交失败: ${errorData.message}`);
    }
  } catch (error) {
    console.error('提交AIGC科普答题记录时发生错误:', error);
    alert('提交答题记录时发生错误，请稍后重试');
  }
};
</script>

<style scoped>
.quiz-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: start;
  min-height: 100vh;
}

.submit-section {
  text-align: center;
}

.submit-section p {
  font-size: 1.2rem;
  margin-bottom: 20px;
}

.submit-section button {
  font-size: 1.2rem;
  padding: 0.8rem 1.6rem;
  background-color: #C5262D;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-section button:hover {
  background-color: #a60030;
}

.question {
  background-color: #fff;
  padding: 1.2rem 1.5rem 1.5rem 1.5rem;
  border-radius: 16px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.06);
  width: 95%;
  box-sizing: border-box;
  max-width: 600px;
  margin: 1.2rem auto;
  text-align: left;
  border: 1px solid #EFF3FF;
  position: relative;
  overflow: hidden;
}

.question::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, #3B82F6, #93C5FD);
}

.q-count {
  position: relative;
  font-size: 1.2rem;
  margin-bottom: 1.2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #EDF2F7;
  color: #4B5563;
  display: flex;
  align-items: center;
}

.q-count span {
  font-size: 2rem;
  color: #3B82F6;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  font-weight: bold;
  background-color: rgba(59, 130, 246, 0.08);
  margin-right: 8px;
}

.q-text {
  font-weight: 600;
  font-size: 1.2rem;
  line-height: 1.6;
  color: #374151;
  margin-bottom: 1.5rem;
}

.buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 1.5rem;
}

.btn {
  font-size: 1rem;
  padding: 0.8rem 1.8rem;
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  font-weight: 500;
  box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
}

.btn-next, .btn-final {
  background: linear-gradient(to right, #3B82F6, #60A5FA);
}

.btn-pre {
  border: 1px solid #3B82F6;
  background-color: white;
  color: #3B82F6;
  box-shadow: none;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.btn-pre:hover {
  background-color: #F5F9FF;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2);
}

.btn:disabled {
  background-color: #E5E7EB;
  cursor: not-allowed;
  box-shadow: none;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1rem;
}

.option {
  margin-bottom: 0;
  background: #F9FAFB;
  border-radius: 10px;
  border: 1px solid #E5E7EB;
  color: #4B5563;
  transition: all 0.2s ease;
}

.option:hover:not(.checked) {
  border-color: #BFDBFE;
  background-color: #F5F9FF;
}

.option.checked {
  border: 1px solid #3B82F6;
  background-color: rgba(59, 130, 246, 0.08);
  color: #3B82F6;
  font-weight: 500;
}

label.radio-label {
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  padding: 1.2rem 1rem;
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

input[type="radio"] {
  margin-right: 10px;
  appearance: none;
  cursor: pointer;
  width: 20px;
  height: 20px;
  border: 2px solid #D1D5DB;
  border-radius: 50%;
  position: relative;
  transition: all 0.2s ease;
}

input[type="radio"]:checked {
  border-color: #3B82F6;
  background-color: white;
}

input[type="radio"]:checked::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #3B82F6;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  margin-top: 100px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3B82F6;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  text-align: center;
  padding: 2rem;
  margin-top: 100px;
}

.error-message p {
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #4B5563;
}

.error-message button {
  font-size: 1rem;
  padding: 0.8rem 1.6rem;
  background-color: #C5262D;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.error-message button:hover {
  background-color: #a60030;
}

</style>
