import { mount } from '@vue/test-utils';
import formula from '@/components/Parents/formula.vue';
import Vue from '../node_modules/vue';

describe('formula.vue', () => {
  const wrapper = mount(formula);
  it('watch the formula value', (done) => {
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
