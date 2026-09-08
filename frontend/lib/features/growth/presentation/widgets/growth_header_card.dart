import 'package:flutter/material.dart';

import '../../data/models/growth_model.dart';



class GrowthHeaderCard extends StatelessWidget {

  final GrowthMetadata metadata;


  const GrowthHeaderCard({
    super.key,
    required this.metadata,
  });



  @override
  Widget build(
    BuildContext context,
  ){

    return Container(

      padding:
          const EdgeInsets.all(24),


      decoration:
          BoxDecoration(

            color:
              Colors.white,

            borderRadius:
              BorderRadius.circular(24),

          ),


      child: Column(

        crossAxisAlignment:
            CrossAxisAlignment.start,


        children:[


          const Text(
            'Growth Analysis',
            style:
              TextStyle(
                fontSize:22,
                fontWeight:
                    FontWeight.bold,
              ),
          ),


          const SizedBox(
            height:20,
          ),


          Text(
            '데이터 신뢰도',
            style:
              TextStyle(
                color:
                  Colors.grey[600],
              ),
          ),


          const SizedBox(
            height:8,
          ),


          Text(

            '${metadata.confidence}%',

            style:
              const TextStyle(

                fontSize:36,

                fontWeight:
                  FontWeight.bold,

              ),

          ),


          const SizedBox(
            height:12,
          ),


          Text(
            metadata.analysisVersion,
          ),


          Text(
            metadata.llmModel,
            style:
              const TextStyle(
                color:
                  Colors.grey,
              ),
          ),

        ],

      ),

    );

  }

}