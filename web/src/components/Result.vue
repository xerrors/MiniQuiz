<template>
  <div class="result">
    <div class="score">
      <div>成绩：<span>{{ score }}</span>分（{{ correctAnswers }} / {{ questions.length }}）</div>
    </div>
    <div class="scorebar">
      <div v-for="(q, index) in questions.length" :key="index" class="scorebar__item" :class="{'item_correct': isCorrect(index)}"></div>
    </div>
    <div class="question-result" v-for="(question, index) in questions" :key="index"
      :class="{'correct__card': isCorrect(index), 'incorrect__card': !isCorrect(index)}">
      <h3>题目 {{ question.序号 }}: {{ question.题目 }}</h3>
      <p>回答:
        <span :class="{'correct': isCorrect(index), 'incorrect': !isCorrect(index)}">{{ answers[index] + ". " + question[answers[index]] }}</span>
        <span></span>
        <span v-if="isCorrect(index)" class="correct">✅</span>
      </p>
      <p v-if="!isCorrect(index)">答案: <span class="correct">{{ question.答案 + ". " + question[question.答案] }}</span></p>
    </div>
    <button v-if="isHistory" @click="goBack">返回</button>
    <button v-else @click="goHome">返回首页</button>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const score = ref(0);
const answers = JSON.parse(route.query.answers);
const questions = JSON.parse(route.query.questions);
const isHistory = route.query.isHistory;

const correctAnswers = computed(() =>
  answers.filter((answer, index) => answer === questions[index].答案).length
);

const isCorrect = (index) => answers[index] === questions[index].答案;


const goHome = () => {
  router.push('/');
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  score.value = Math.round(correctAnswers.value / questions.length * 100);
});
</script>

<style scoped>
.result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 1rem;
  box-sizing: border-box;
  margin-top: 0;
  transition: margin-top 0.3s ease;
}

.result .score {
  padding: 2.5rem 0;
  font-size: 1.4rem;
  color: #4B5563;
  margin-bottom: 1.5rem;
  margin-top: 1rem;
  position: relative;
}

.result .score span {
  font-size: 3.5rem;
  font-weight: bold;
  color: #3B82F6;
  display: block;
  margin: 0.5rem 0;
  text-shadow: 0 2px 10px rgba(59, 130, 246, 0.2);
}

.scorebar {
  margin-bottom: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.3rem;
  width: 100%;
  max-width: 600px;
  padding: 0 1rem;
  box-sizing: border-box;
}

.scorebar > .scorebar__item {
  width: 2px;
  height: 0.8rem;
  flex-grow: 1;
  display: inline-block;
  border-radius: 4px;
  background-color: #EDF2F7;
  opacity: 0.8;
  transition: all 0.2s ease;
}

.scorebar > .scorebar__item.item_correct {
  background-color: #3B82F6;
  height: 1.2rem;
  opacity: 1;
}

p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.question-result {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  margin-bottom: 2rem;
  text-align: left;
  width: 100%;
  max-width: 600px;
  box-sizing: border-box;
  font-size: 1rem;
  font-weight: 300;
  position: relative;
  overflow: hidden;
  border: 1px solid #EDF2F7;
  transition: all 0.2s ease;
}

.question-result:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.08);
}

.question-result.correct__card {
  background-color: rgba(59, 130, 246, 0.04);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.08);
  border: 1px solid rgba(59, 130, 246, 0.2);
}

.question-result.correct__card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, #3B82F6, #60A5FA);
}

.question-result.incorrect__card {
  background-color: rgba(239, 68, 68, 0.04);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.08);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

.question-result.incorrect__card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(to right, #EF4444, #F87171);
}

.question-result h3 {
  color: #374151;
  margin-top: 0.5rem;
  margin-bottom: 1rem;
  font-size: 1.15rem;
  line-height: 1.5;
}

.question-result p {
  margin: 0.8rem 0;
  font-size: 1.05rem;
  color: #4B5563;
  line-height: 1.5;
}

.question-result p span.correct {
  color: #3B82F6;
  font-weight: 500;
  display: inline-block;
  padding: 0.3rem 0.5rem;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 4px;
  margin-left: 0.5rem;
}

.question-result p span.incorrect {
  color: #EF4444;
  font-weight: 500;
  display: inline-block;
  padding: 0.3rem 0.5rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-radius: 4px;
  margin-left: 0.5rem;
}

button {
  font-size: 1.1rem;
  padding: 0.9rem 2rem;
  background: linear-gradient(to right, #3B82F6, #60A5FA);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  width: 100%;
  max-width: 600px;
  font-weight: 500;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3);
}

button:hover {
  background: linear-gradient(to right, #2563EB, #3B82F6);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}
</style>
