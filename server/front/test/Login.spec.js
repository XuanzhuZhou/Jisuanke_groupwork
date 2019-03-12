import { mount } from '@vue/test-utils';
import login from '@/components/BackLogin/Login.vue';

describe('tab-pane', () => {
  const wrapper = mount(login);
  it('角色转换', () => {
    expect(wrapper.vm.ruleForm2.user).toBe('');
    const button = wrapper.find('el-tab-pane');
    button.trigger('click');
    expect(wrapper.vm.ruleForm2.pass).toBe('');
  });
});

describe('Login', () => {
  const wrapper = mount(login);
  it('属性', () => {
    const tabs = wrapper.find('el-button');
    expect(tabs.text()).toBe('登录');
  });
});
