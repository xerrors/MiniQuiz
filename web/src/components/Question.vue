<template>
  <div class="question">
    <h3 class="q-text"><span>第{{ (currentQuestionIndex+1) }}题</span>{{ question.题目 }}</h3>
    <div class="options">
      <div v-for="(option, name) in optionsLabel" :key="name" class="option" :class="{ checked: isChecked(name) }">
        <label class="radio-label">
          <input type="radio"
                :value="name" v-model="selectedAnswer"/>
          {{ name + " " + option }}
        </label>
      </div>
    </div>
    <button class="btn-next" @click="submitAnswer" :disabled="!selectedAnswer">下一题</button>
    <!-- <button class="btn-prev" @click="preAnswer" v-if="currentQuestionIndex > 0">上一题</button> -->
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  question: Object,
  currentQuestionIndex: Number,
});
const emit = defineEmits(['answered']);

const selectedAnswer = ref('');
const isChecked = (name) => selectedAnswer.value === name;

const optionsLabel = computed(() => {
  return {
    A: props.question.A,
    B: props.question.B,
    C: props.question.C,
    D: props.question.D,
  };
});

console.log(props.question);

const submitAnswer = () => {
  if (selectedAnswer.value) {
    emit('answered', selectedAnswer.value);
    selectedAnswer.value = '';  // 清空选择的答案
  }
};

const preAnswer = () => {
  emit('prev');
};
</script>

<style scoped>
.question {
  background-color: #fff;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  max-width: 600px;
  margin: 1rem auto;
  text-align: left;
}

.q-text {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.q-text span {
  font-size: 1.2rem;
  color: #C5262D;
  margin-right: 0.5rem;
  background-color: #f9f9f9;
  padding: 0.1rem 0.5rem;
  border-radius: 8px;

}

.btn-next {
  font-size: 1rem;
  padding: 0.8rem 1.6rem;
  background-color: #C5262D;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-next:disabled {
  background-color: #ddd;
  cursor: not-allowed;
}

.btn-next:not(:disabled):hover {
  background-color: #a60030;
}

.btn-prev {
  font-size: 1.2rem;
  padding: 0.8rem 1.6rem;
  color: #C5262D;
  border: none;
  cursor: pointer;
  background-color: transparent;
}


.options {
  display: flex;
  flex-direction: column;
  gap: 0.3rem; /* 设置选项之间的间距 */
  margin-bottom: 1rem;
}

.option {
  margin-bottom: 0.5rem;
  background: #f6f4f2;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.01)
}

.option.checked {
  background-color: #C5262D;
  color: white;
}

label.radio-label {
  font-size: 1rem;
  width: 100%;
  /* border: 1px solid #ccc; */
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer; /* 添加鼠标指针样式 */
  padding: 1rem 0;
}

input[type="radio"] {
  margin-right: 10px;
  appearance: none; /* 移除默认的圆框 */
  cursor: pointer;
}

input[type="radio"]:checked::label.radio-label {
  background: #C5262D;
  color: white;
}


</style>
