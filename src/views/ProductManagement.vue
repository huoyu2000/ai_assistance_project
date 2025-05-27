// 选项卡
const tabs = [
  { id: 'all', name: '所有产品' },
  { id: 'category', name: '分类管理' },
  { id: 'recipe', name: '菜谱' },
  { id: 'pricing', name: '定价' }
];
const activeTab = ref('category'); // 默认显示分类管理 