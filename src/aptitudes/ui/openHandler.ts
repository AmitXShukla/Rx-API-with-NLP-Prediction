import { ui } from '@oliveai/ldk';
import {
  networkExample
} from '../../aptitudes';

import { IntroWhisper } from '../../whispers';

export const handler = async () => {
  new IntroWhisper().show();
  // networkExample.run();
};

export default {
  start: () => ui.loopOpenHandler(handler),
};
