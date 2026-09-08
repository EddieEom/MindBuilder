import 'package:flutter/material.dart';

import '../../data/models/growth_model.dart';


class GrowthItemCard extends StatelessWidget {

  final GrowthItem item;


  const GrowthItemCard({
    super.key,
    required this.item,
  });



  Color _getColor(){

    switch(item.type){

      case 'unlearning':
        return const Color(0xFFE57373);

      case 'relearning':
        return const Color(0xFF64B5F6);

      case 'newlearning':
        return const Color(0xFF81C784);

      default:
        return const Color(0xFF9E9E9E);

    }

  }



  String _getLabel(){

    switch(item.type){

      case 'unlearning':
        return 'Unlearning';

      case 'relearning':
        return 'Relearning';

      case 'newlearning':
        return 'Newlearning';

      default:
        return item.type;

    }

  }



  @override
  Widget build(
    BuildContext context,
  ){

    return Container(

      margin:
          const EdgeInsets.only(
            bottom:16,
          ),


      padding:
          const EdgeInsets.all(20),


      decoration:
          BoxDecoration(

            color:
                Colors.white,

            borderRadius:
                BorderRadius.circular(20),

            border:
                Border.all(
                  color:
                    _getColor()
                    .withValues(alpha : 0.3),
                ),

          ),


      child: Column(

        crossAxisAlignment:
            CrossAxisAlignment.start,


        children:[


          Row(

            children:[

              Container(

                padding:
                    const EdgeInsets.symmetric(
                      horizontal:12,
                      vertical:6,
                    ),

                decoration:
                    BoxDecoration(

                      color:
                        _getColor()
                        .withValues(alpha : 0.15),

                      borderRadius:
                        BorderRadius.circular(20),

                    ),

                child:
                    Text(

                      _getLabel(),

                      style:
                        TextStyle(
                          color:
                            _getColor(),

                          fontWeight:
                            FontWeight.bold,
                        ),

                    ),

              ),


              const Spacer(),


              Text(
                'Priority ${item.priority}',
                style:
                    const TextStyle(
                      color:
                        Colors.grey,
                    ),
              ),

            ],

          ),


          const SizedBox(
            height:16,
          ),


          Text(

            item.title,

            style:
                const TextStyle(

                  fontSize:20,

                  fontWeight:
                      FontWeight.bold,

                ),

          ),


          const SizedBox(
            height:12,
          ),


          Text(

            item.content,

            style:
                const TextStyle(

                  fontSize:15,

                  height:1.5,

                  color:
                      Color(0xFF555555),

                ),

          ),


        ],

      ),

    );

  }

}