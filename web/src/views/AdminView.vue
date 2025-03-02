<template>
  <div class="admin-container">
    <h1 class="title">管理员界面</h1>
    <div class="admin-tabs">
      <button
        :class="['tab-button', { active: activeTab === 'class' }]"
        @click="activeTab = 'class'"
      >
        班级答题情况
      </button>
      <button
        :class="['tab-button', { active: activeTab === 'user' }]"
        @click="activeTab = 'user'"
      >
        用户答题情况
      </button>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>正在加载数据...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- 班级答题情况 -->
    <div v-if="activeTab === 'class' && !loading" class="data-panel">
      <div class="card stats-card">
        <h2>班级统计概览</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-value">{{ classStats.totalClasses }}</div>
            <div class="stat-label">班级总数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ classStats.totalStudents }}</div>
            <div class="stat-label">学生总数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ classStats.totalRecords }}</div>
            <div class="stat-label">答题记录数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ classStats.avgScore.toFixed(1) }}</div>
            <div class="stat-label">平均分数</div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2>各班级答题情况</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>班级</th>
              <th>学生人数</th>
              <th>答题人数</th>
              <th>答题次数</th>
              <th>平均分数</th>
              <th>最高分数</th>
              <th>参与率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stats, className) in classSummary" :key="className">
              <td>{{ className }}</td>
              <td>{{ stats.totalStudents }}</td>
              <td>{{ stats.activeStudents }}</td>
              <td>{{ stats.totalRecords }}</td>
              <td>{{ stats.avgScore.toFixed(1) }}</td>
              <td>{{ stats.maxScore }}</td>
              <td>{{ (stats.activeStudents / stats.totalStudents * 100).toFixed(1) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 用户答题情况 -->
    <div v-if="activeTab === 'user' && !loading" class="data-panel">
      <div class="search-filter">
        <input
          type="text"
          v-model="userFilter"
          placeholder="输入姓名或学号筛选..."
          class="search-input"
        />
        <select v-model="classFilter" class="class-select">
          <option value="">所有班级</option>
          <option v-for="className in classNames" :key="className" :value="className">
            {{ className }}
          </option>
        </select>
        <select v-model="sortOption" class="sort-select">
          <option value="class">按班级排序</option>
          <option value="sid">按学号排序</option>
          <option value="name">按姓名排序</option>
          <option value="recordCount">按答题次数排序</option>
          <option value="avgScore">按平均分数排序</option>
          <option value="maxScore">按最高分数排序</option>
        </select>
        <button @click="toggleSortOrder" class="sort-btn">
          {{ sortAscending ? '升序 ▲' : '降序 ▼' }}
        </button>
      </div>

      <div class="card">
        <h2>用户答题详情</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>学号</th>
              <th>姓名</th>
              <th>班级</th>
              <th>答题次数</th>
              <th>最近答题</th>
              <th>平均分数</th>
              <th>最高分数</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.sid">
              <td>{{ user.sid }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.class }}</td>
              <td>{{ user.records.length }}</td>
              <td>{{ user.records.length ? formatDate(user.records[0].date) : '-' }}</td>
              <td>{{ user.avgScore.toFixed(1) }}</td>
              <td>{{ user.maxScore }}</td>
              <td>
                <button class="detail-btn" @click="showUserDetail(user)">查看详情</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 用户详情弹窗 -->
    <div v-if="showDetailModal" class="modal">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ selectedUser.name }} ({{ selectedUser.sid }}) 的答题记录</h2>
          <button class="close-btn" @click="showDetailModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <table class="detail-table">
            <thead>
              <tr>
                <th>答题时间</th>
                <th>分数</th>
                <th>答题题目数</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(record, index) in selectedUser.records" :key="index">
                <td>{{ formatDate(record.date) }}</td>
                <td>{{ record.score }}</td>
                <td>{{ JSON.parse(record.questions).length }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// 状态变量
const records = ref([]);
const users = ref([]);
const loading = ref(true);
const error = ref('');
const activeTab = ref('class');
const userFilter = ref('');
const classFilter = ref('');
const showDetailModal = ref(false);
const selectedUser = ref(null);
const sortOption = ref('class');
const sortAscending = ref(true);

// 获取用户数据和答题记录
const fetchData = async () => {
  loading.value = true;
  error.value = '';

  try {
    // 获取登录用户信息
    const userCookie = document.cookie.split('; ').find(row => row.startsWith('user='));
    if (!userCookie) {
      error.value = '您需要先登录';
      loading.value = false;
      return;
    }

    const user = JSON.parse(decodeURIComponent(userCookie.split('=')[1]));
    if (user.role !== 'admin') {
      error.value = '您没有管理员权限';
      loading.value = false;
      return;
    }

    // 获取所有答题记录
    const response = await fetch('/api/admin_get_records', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({ sid: user.sid }),
    });

    const data = await response.json();
    if (!data.ok) {
      throw new Error(data.message || '获取记录失败');
    }

    records.value = data.data;

    // 查找所有用户数据
    await fetchUserData();

    // 处理数据
    processData();

  } catch (err) {
    console.error('获取数据失败:', err);
    error.value = '获取数据失败: ' + (err.message || '未知错误');
  } finally {
    loading.value = false;
  }
};

// 获取用户数据
const fetchUserData = async () => {
  try {
    const response = await fetch('/api/get_all_users', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
      body: JSON.stringify({
        sid: JSON.parse(decodeURIComponent(document.cookie.split('; ')
          .find(row => row.startsWith('user='))
          .split('=')[1])).sid
      }),
    });

    const data = await response.json();
    if (!data.ok) {
      throw new Error(data.message || '获取用户数据失败');
    }

    users.value = data.users;
  } catch (err) {
    console.error('获取用户数据失败:', err);
    error.value = '获取用户数据失败: ' + (err.message || '未知错误');
  }
};

// 处理数据，整合用户和记录
const processData = () => {
  // 处理用户数据，添加答题记录
  users.value.forEach(user => {
    const userRecords = records.value.filter(record => record.sid === user.sid);
    user.records = userRecords.sort((a, b) => new Date(b.date) - new Date(a.date));
    user.avgScore = userRecords.length
      ? userRecords.reduce((sum, r) => sum + parseScore(r.score), 0) / userRecords.length
      : 0;
    user.maxScore = userRecords.length
      ? Math.max(...userRecords.map(r => parseScore(r.score)))
      : 0;
  });
};

// 新增：解析分数字符串的函数
const parseScore = (scoreStr) => {
  if (!scoreStr) return 0;

  // 处理"7 / 20"格式的分数
  const parts = scoreStr.split('/');
  if (parts.length === 2) {
    const numerator = parseFloat(parts[0].trim());
    const denominator = parseFloat(parts[1].trim());
    if (!isNaN(numerator) && !isNaN(denominator) && denominator !== 0) {
      return numerator / denominator * 100; // 转换为百分制分数
    }
  }

  // 尝试直接解析为数字
  const score = parseFloat(scoreStr);
  return isNaN(score) ? 0 : score;
};

// 班级统计数据
const classSummary = computed(() => {
  const summary = {};

  // 初始化班级统计
  users.value.forEach(user => {
    if (!summary[user.class]) {
      summary[user.class] = {
        totalStudents: 0,
        activeStudents: 0,
        totalRecords: 0,
        scores: [],
        avgScore: 0,
        maxScore: 0
      };
    }
    summary[user.class].totalStudents += 1;

    const userRecords = records.value.filter(r => r.sid === user.sid);
    if (userRecords.length > 0) {
      summary[user.class].activeStudents += 1;
      summary[user.class].totalRecords += userRecords.length;

      userRecords.forEach(record => {
        summary[user.class].scores.push(parseScore(record.score));
      });
    }
  });

  // 计算平均分和最高分
  Object.values(summary).forEach(stats => {
    stats.avgScore = stats.scores.length
      ? stats.scores.reduce((sum, score) => sum + score, 0) / stats.scores.length
      : 0;
    stats.maxScore = stats.scores.length
      ? Math.max(...stats.scores)
      : 0;
  });

  return summary;
});

// 总体统计数据
const classStats = computed(() => {
  const stats = {
    totalClasses: Object.keys(classSummary.value).length,
    totalStudents: users.value.length,
    totalRecords: records.value.length,
    avgScore: records.value.length
      ? records.value.reduce((sum, r) => sum + parseScore(r.score), 0) / records.value.length
      : 0
  };

  return stats;
});

// 班级名称列表
const classNames = computed(() => {
  return [...new Set(users.value.map(user => user.class))];
});

// 筛选后的用户列表
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const matchesFilter = user.name.includes(userFilter.value) ||
                          user.sid.includes(userFilter.value);
    const matchesClass = !classFilter.value || user.class === classFilter.value;
    return matchesFilter && matchesClass;
  }).sort((a, b) => {
    // 根据选择的排序选项进行排序
    let comparison = 0;

    switch (sortOption.value) {
      case 'sid':
        comparison = a.sid.localeCompare(b.sid);
        break;
      case 'name':
        comparison = a.name.localeCompare(b.name);
        break;
      case 'class':
        comparison = a.class.localeCompare(b.class);
        if (comparison === 0) {
          comparison = a.name.localeCompare(b.name); // 班级相同时按姓名排序
        }
        break;
      case 'recordCount':
        comparison = a.records.length - b.records.length;
        break;
      case 'avgScore':
        comparison = a.avgScore - b.avgScore;
        break;
      case 'maxScore':
        comparison = a.maxScore - b.maxScore;
        break;
      default:
        comparison = a.class.localeCompare(b.class);
    }

    // 根据排序顺序返回比较结果
    return sortAscending.value ? comparison : -comparison;
  });
});

// 显示用户详情
const showUserDetail = (user) => {
  selectedUser.value = user;
  showDetailModal.value = true;
};

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
};

// 页面加载时获取数据
onMounted(() => {
  fetchData();
});

// 排序选项
const toggleSortOrder = () => {
  sortAscending.value = !sortAscending.value;
};
</script>

<style scoped>
.admin-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #2563EB;
}

.admin-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.tab-button {
  padding: 12px 24px;
  background-color: #f0f9ff;
  border: none;
  cursor: pointer;
  font-size: 16px;
  flex: 1;
  transition: all 0.3s ease;
}

.tab-button.active {
  background-color: #2563EB;
  color: white;
  font-weight: bold;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid #2563EB;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  margin: 20px 0;
}

.data-panel {
  margin-top: 20px;
}

.card {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
  padding: 20px;
}

.card h2 {
  color: #2563EB;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.2rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 10px;
}

.stats-card {
  background: linear-gradient(to right, #f0f9ff, #e0f2fe);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.stat-item {
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.stat-value {
  font-size: 1.8rem;
  font-weight: bold;
  color: #2563EB;
  margin-bottom: 5px;
}

.stat-label {
  color: #6b7280;
  font-size: 0.9rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.data-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #4b5563;
}

.data-table tr:hover {
  background-color: #f1f5f9;
}

.search-filter {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-input, .class-select {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
}

.search-input {
  flex: 1;
}

.class-select {
  min-width: 150px;
}

.sort-select {
  min-width: 160px;
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  background-color: #f8fafc;
}

.sort-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 10px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.sort-btn:hover {
  background-color: #2563eb;
}

.detail-btn {
  background-color: #2563EB;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background-color 0.2s;
}

.detail-btn:hover {
  background-color: #1d4ed8;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  width: 80%;
  max-width: 800px;
  max-height: 90vh;
  overflow: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #2563EB;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6b7280;
}

.modal-body {
  padding: 20px;
}

.detail-table {
  width: 100%;
  border-collapse: collapse;
}

.detail-table th, .detail-table td {
  padding: 10px 15px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.detail-table th {
  background-color: #f8fafc;
  font-weight: 600;
  color: #4b5563;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .search-filter {
    flex-direction: column;
    gap: 10px;
  }

  .search-input, .class-select, .sort-select, .sort-btn {
    width: 100%;
  }

  .data-table {
    font-size: 14px;
  }

  .card {
    padding: 15px;
    overflow-x: auto;
  }

  .data-table {
    min-width: 650px;
  }

  .data-table th, .data-table td {
    white-space: nowrap;
  }

  .modal-body {
    padding: 15px;
    overflow-x: auto;
  }

  .detail-table {
    min-width: 500px;
  }

  .detail-table th, .detail-table td {
    white-space: nowrap;
  }
}
</style>