import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro-humanoid-robotics',      // Module 1
    {
      type: 'category',
      label: 'Module 2: Kinematics and Motion',
      link: {
        type: 'generated-index',
        title: 'Kinematics and Motion',
        description: 'Learn about the principles of humanoid robot kinematics and motion.',
        slug: '/category/kinematics-and-motion',
      },
      items: [
        'module2/forward-kinematics',
        'module2/inverse-kinematics',
      ],
    },
    {
      type: 'category',
      label: 'Module 3: Sensors and Perception',
      link: {
        type: 'generated-index',
        title: 'Sensors and Perception',
        description: 'Learn about sensors and perception algorithms in humanoid robots.',
        slug: '/category/sensors-and-perception',
      },
      items: [
        'module3/sensor-types',
        'module3/basic-localization',
      ],
    },
    {
      type: 'category',
      label: 'Module 4: Actuation and Control',
      link: {
        type: 'generated-index',
        title: 'Actuation and Control',
        description: 'Learn about actuation and control systems in humanoid robots.',
        slug: '/category/actuation-and-control',
      },
      items: [
        'module4/actuator-types',
        'module4/pid-control',
      ],
    },
    // 'kinematics-motion',            // Module 2
    // 'sensors-perception',           // Module 3
    // 'actuation-control',            // Module 4
  ],
};

export default sidebars;
