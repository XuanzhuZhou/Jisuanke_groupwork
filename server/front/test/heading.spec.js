import { mount } from '@vue/test-utils';
import heading from '@/components/Landing/heading.vue';

describe('heading.vue', () => {
  const wrapper = mount(heading);
  it('ladding page', () => {
    expect(wrapper.findAll('el-menu-item').at(1).text()).toBe('首页');
  });
});

describe('heading test', () => {
  const wrapper = mount(heading);
  it('test the show function', () => {
    const button = wrapper.findAll('el-menu-item').at(2);
    button.trigger('click');
    expect(wrapper.vm.initial).toBe('1');
  });
});
