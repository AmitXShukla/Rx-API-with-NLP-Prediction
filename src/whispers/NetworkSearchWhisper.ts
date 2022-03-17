import { whisper } from '@oliveai/ldk';
import { stripIndent } from 'common-tags';

type Recall = {
  [key: string]: string;
};
interface Props {
  recalls: Recall[];
}
export default class NetworkSearchWhisper {
  whisper: whisper.Whisper;
  label: string;
  props: Props;

  constructor(recalls: Recall[]) {
    this.whisper = undefined;
    this.label = 'CT.gov Search Results';
    this.props = {
      recalls,
    };
  }
  createComponents() {
    const components = [];
    this.props.recalls.forEach((recall) => {

      try {
        components.push({
          type: whisper.WhisperComponentType.Link,
          text: `${recall.NCTId[0]} - ${recall.Condition[0]}`,
          onClick: () => {
            const markdown = stripIndent`
  
  **BriefTitle:** ${recall.BriefTitle[0]}
  
  **OverallStatus:** ${recall.OverallStatus[0]}
  
  **StartDate:** ${recall.StartDate[0]}
  
  **CompletionDate:** ${recall.CompletionDate[0]}
  
  **LeadSponsorName:** ${recall.LeadSponsorName[0]}
  
  **BriefSummary:** ${recall.BriefSummary[0].replace("<", " ")}
  
  **DetailedDescription:** ${recall.DetailedDescription[0]}
  
  # NLP ALERTS
  ## matching studies - on-premise DB
  none
  `;
            whisper.create({
              label: `Details for ${recall.NCTId[0]} - ${recall.Condition[0]}`,
              components: [
                {
                  type: whisper.WhisperComponentType.Markdown,
                  body: markdown,
                },
              ],
            });
          },
        });
      } catch (error) {
        components.push({
          type: whisper.WhisperComponentType.Link,
          text: `no results returned.`
        });
      }
    });

    return components;
  }
  // createComponents() {
  //   const components = [];
  //   this.props.recalls.forEach((recall) => {
  //     components.push({
  //       type: whisper.WhisperComponentType.Link,
  //       text: `${recall.recalling_firm} (${recall.recall_initiation_date})`,
  //       onClick: () => {
  //         const markdown = stripIndent`
  //         # Recalling Firm
  //         ${recall.recalling_firm}
  //         # Recall Number
  //         ${recall.recall_number}
  //         # Product Description
  //         ${recall.product_description}
  //         # Reason for Recall
  //         ${recall.reason_for_recall}
  //         `;

  //         whisper.create({
  //           label: `Recall for ${recall.recalling_firm}`,
  //           components: [
  //             {
  //               type: whisper.WhisperComponentType.Markdown,
  //               body: markdown,
  //             },
  //           ],
  //         });
  //       },
  //     });
  //   });

  //   return components;
  // }

  show() {
    whisper
      .create({
        components: this.createComponents(),
        label: this.label,
        onClose: NetworkSearchWhisper.onClose,
      })
      .then((newWhisper) => {
        this.whisper = newWhisper;
      });
  }

  close() {
    this.whisper.close(NetworkSearchWhisper.onClose);
  }

  static onClose(err?: Error) {
    if (err) {
      console.error('There was an error closing Network whisper', err);
    }
    // console.log('Network whisper closed');
  }
}
