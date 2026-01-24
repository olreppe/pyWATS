using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace Virinco.WATS.Interface
{

    public static class Util
    {
        [DebuggerStepThrough]
        public static T[] SubArray<T>(this T[] data, int index, int length)
        {
            T[] result = new T[length];
            Array.Copy(data, index, result, 0, length);
            return result;
        }
    }

    public class GroupMatch
    {
        public string GroupString { get; set; }
        public int MatchPos { get; set; }
    }


    class SequenceTree
    {

        public string RootName { get; set; }
        public int fromStepOrder, toStepOrder;
        public int occurrences = 0;
        public int matchPos;
        public List<SequenceTree> Children { get; set; }

        public SequenceTree(GroupMatch[] match, int stepOrder)
        {
            if (match.Length > 0)
            {
                RootName = match[0].GroupString;
                fromStepOrder = toStepOrder = stepOrder;
                if (match.Length > 1 && Children == null)
                {
                    Children = new List<SequenceTree>();
                }
            }
        }       
        public void AddChildren(GroupMatch[] names, int stepOrder)
        {
            if (Children == null)
                Children = new List<SequenceTree>();
            SequenceTree sequenceTree = Children.Where(c => c.RootName == names[0].GroupString).FirstOrDefault();
            if (sequenceTree == null)
            {
                sequenceTree = new SequenceTree(names, stepOrder);
                Children.Add(sequenceTree);
            }
            toStepOrder = stepOrder;
            if (names.Length > 1)
                sequenceTree.AddChildren(Util.SubArray<GroupMatch>(names, 1, names.Length - 1), stepOrder);
        }

        string GetFullNameFromMatch(GroupMatch match, string fullName)
        {
            if (match == null)
                return fullName;
            else 
                return fullName.Substring(0, match.MatchPos + match.GroupString.Length);
        }

        internal string GetName(GroupMatch[] names, string fullName)
        {
            if (Children == null || Children.Count > 1 || names.Length<1)
                return names.Length==0 ? GetFullNameFromMatch(null, fullName):GetFullNameFromMatch(names[0], fullName);
            //Children=1, so far unique
            return Children.First().GetName(Util.SubArray<GroupMatch>(names, 1, names.Length - 1), fullName);
        }
    }
    

    public class SequenceGrouper
    {
        Regex groupingRegex;
        List<SequenceTree> rootSequences;

        public SequenceGrouper(string groupingRegExpression = @"([^_ ]+?)[_ ]+")
        {
            groupingRegex = new Regex(groupingRegExpression);
            rootSequences = new List<SequenceTree>();
        }

        GroupMatch[] GetParts(string stepName)
        {
            MatchCollection matches = groupingRegex.Matches(stepName);
            List<GroupMatch> groupMatches = new List<GroupMatch>();
            if (matches.Count == 0 || matches[0].Groups.Count < 2)
            {
                groupMatches.Add(new GroupMatch { GroupString = stepName, MatchPos = 0 });
            }
            else
                foreach (Match match in matches)
                {
                    groupMatches.Add(new GroupMatch { GroupString = match.Groups[1].Value, MatchPos = match.Groups[1].Index});
                }
            return groupMatches.ToArray();
        }
        
        SequenceTree prevStepRoot = null;
        public void RegisterStepName(string stepName, int stepOrder)
        {
            GroupMatch[] nameParts = GetParts(stepName);
            SequenceTree sequenceTree;
            if (prevStepRoot == null || prevStepRoot.RootName != nameParts[0].GroupString)
            {
                sequenceTree = new SequenceTree(nameParts, stepOrder);
                rootSequences.Add(sequenceTree);
            }
            else
                sequenceTree = rootSequences.Last();
            if (nameParts.Length > 1)
                sequenceTree.AddChildren(Util.SubArray<GroupMatch>(nameParts, 1, nameParts.Length - 1), stepOrder);
            else
                sequenceTree.toStepOrder = stepOrder;
            sequenceTree.occurrences++;
            prevStepRoot = sequenceTree;
        }

        public string GetSequenceGroup(string stepName, int stepOrder)
        {
            GroupMatch[] nameParts = GetParts(stepName);
            SequenceTree rootSequence = rootSequences.Where(s => s.RootName == nameParts[0].GroupString && stepOrder>=s.fromStepOrder && stepOrder<=s.toStepOrder).FirstOrDefault();
            if (rootSequence.occurrences == 1)
                return "Main Sequence Callback";
            return rootSequence.GetName(Util.SubArray<GroupMatch>(nameParts, 1, nameParts.Length - 1),stepName);            
        }
    }
}
