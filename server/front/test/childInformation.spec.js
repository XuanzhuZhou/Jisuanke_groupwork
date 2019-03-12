import { mount } from '@vue/test-utils';
import child from '@/components/Parents/childInformation.vue';
import Vue from '../node_modules/vue';

describe('Information.vue', () => {
  const wrapper = mount(child);
  it('changeInformation for children', (done) => {
    wrapper.vm.initial = '2';
    Vue.nextTick(() => {
      expect(wrapper.vm.currValue).toBe('3');
    });
    wrapper.vm.initial = '3';
    Vue.nextTick(() => {
      expect(wrapper.vm.currValue).toBe('3');
      done();
    });
  });
});
