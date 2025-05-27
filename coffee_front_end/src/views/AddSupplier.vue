<template>
  <div class="page-content-container">
    <div class="header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          返回
        </button>
        <h1 class="page-title">添加供应商</h1>
      </div>
    </div>

    <div class="form-container">
      <form @submit.prevent="submitForm" class="supplier-form">
        <div class="form-section">
          <h2 class="section-title">基本信息</h2>
          
          <div class="form-group">
            <label for="supplierName">供应商名称<span class="required">*</span></label>
            <input type="text" id="supplierName" v-model="form.name" required>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="category">供应商类别<span class="required">*</span></label>
              <select id="category" v-model="form.category" required>
                <option value="">请选择类别</option>
                <option value="咖啡豆">咖啡豆</option>
                <option value="牛奶和奶油">牛奶和奶油</option>
                <option value="糖浆和配料">糖浆和配料</option>
                <option value="一次性用品">一次性用品</option>
                <option value="茶类">茶类</option>
                <option value="设备">设备</option>
                <option value="其他">其他</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="status">状态<span class="required">*</span></label>
              <select id="status" v-model="form.status" required>
                <option value="活跃">活跃</option>
                <option value="不活跃">不活跃</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="form-section">
          <h2 class="section-title">联系信息</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="contactName">联系人姓名<span class="required">*</span></label>
              <input type="text" id="contactName" v-model="form.contactName" required>
            </div>
            
            <div class="form-group">
              <label for="contactPhone">联系电话<span class="required">*</span></label>
              <input type="tel" id="contactPhone" v-model="form.contactPhone" required>
            </div>
          </div>
          
          <div class="form-group">
            <label for="contactEmail">电子邮箱</label>
            <input type="email" id="contactEmail" v-model="form.contactEmail">
          </div>
          
          <div class="form-group">
            <label for="address">地址<span class="required">*</span></label>
            <textarea id="address" v-model="form.address" required></textarea>
          </div>
        </div>
        
        <div class="form-section">
          <h2 class="section-title">合同信息</h2>
          
          <div class="form-row">
            <div class="form-group">
              <label for="contractNumber">合同编号</label>
              <input type="text" id="contractNumber" v-model="form.contractNumber">
            </div>
            
            <div class="form-group">
              <label for="startDate">合作起始日<span class="required">*</span></label>
              <input type="date" id="startDate" v-model="form.startDate" required>
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label for="endDate">到期日期</label>
              <input type="date" id="endDate" v-model="form.endDate">
            </div>
            
            <div class="form-group">
              <label for="paymentTerms">付款条件</label>
              <select id="paymentTerms" v-model="form.paymentTerms">
                <option value="">请选择付款条件</option>
                <option value="发票日期后15天内">发票日期后15天内</option>
                <option value="发票日期后30天内">发票日期后30天内</option>
                <option value="发票日期后45天内">发票日期后45天内</option>
                <option value="货到付款">货到付款</option>
                <option value="预付款">预付款</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="goBack">取消</button>
          <button type="submit" class="submit-btn">保存</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// 表单数据
const form = ref({
  name: '',
  category: '',
  status: '活跃',
  contactName: '',
  contactPhone: '',
  contactEmail: '',
  address: '',
  contractNumber: '',
  startDate: '',
  endDate: '',
  paymentTerms: ''
});

// 提交表单
const submitForm = () => {
  // 这里应该添加表单验证逻辑
  console.log('表单数据:', form.value);
  
  // 提交成功后返回列表页面
  router.push('/procurement');
};

// 返回上一页
const goBack = () => {
  router.push('/procurement');
};
</script>

<style scoped>
.page-content-container {
  width: 100%;
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 100%;
  overflow-x: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  flex-wrap: wrap;
  gap: 12px;
  width: 100%;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: var(--secondary-text-color, #638770);
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 8px;
}

.back-btn:hover {
  background-color: var(--sidebar-active-bg, #F0F5F2);
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 24px;
  line-height: 1.25em;
  color: var(--primary-text-color, #121714);
  margin: 0;
}

.form-container {
  padding: 16px;
  overflow-y: auto;
  flex: 1;
}

.supplier-form {
  max-width: 800px;
  margin: 0 auto;
}

.form-section {
  margin-bottom: 32px;
  background-color: var(--content-bg-color, #FFFFFF);
  border: 1px solid var(--border-color, #E5E8EB);
  border-radius: 12px;
  padding: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 20px 0;
  color: var(--primary-text-color, #121714);
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.form-row {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
  margin-bottom: 16px;
}

.form-row .form-group {
  margin-bottom: 0;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
}

.required {
  color: #f44336;
  margin-left: 4px;
}

input, select, textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, #E5E8EB);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
  transition: border-color 0.2s;
  font-family: 'Space Grotesk', sans-serif;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: var(--secondary-text-color, #638770);
}

textarea {
  min-height: 100px;
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 24px;
}

.cancel-btn, .submit-btn {
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  border: none;
  font-family: 'Space Grotesk', sans-serif;
}

.cancel-btn {
  background-color: transparent;
  border: 1px solid var(--border-color, #E5E8EB);
  color: var(--primary-text-color, #121714);
}

.submit-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.submit-btn:hover {
  background-color: var(--secondary-text-color, #638770);
  color: #FFFFFF;
}

@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 16px;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
}
</style> 