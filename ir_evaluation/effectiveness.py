import math

class effectiveness():
    def ap_at_n(self, interactions, boundaries=['all']):
        ap = dict()
        m_ap = dict() # mean ap@n

        for cutoff in boundaries:
            ap[cutoff] = []

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = interactions[query]['visited_documents_orders']

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        related = 0
                        for document_id in visited_documents:
                            if document_id in related_documents and int(visited_documents_orders[document_id]) <= cutoff:
                                related += 1

                        calc = related / cutoff
                        ap[cutoff].append(calc)
                else:
                    related = 0
                    for document_id in visited_documents:
                        if document_id in related_documents:
                            related += 1

                    calc = related / total_result
                    ap[cutoff].append(calc)

        # m_ap calculation over all organised ap values
        for cutoff in boundaries:
            m_ap[cutoff] = {'count': 0, 'value': 0}

            # is there any value for the related cutoff
            if len(ap[cutoff]) > 0:
                m_ap[cutoff]['count'] = len(ap[cutoff])
                m_ap[cutoff]['value'] = sum(ap[cutoff]) / len(ap[cutoff])

        return m_ap

    def mean_ap(self, interactions, boundaries=['all']):
        ap = dict()
        mean_ap = dict() # mean ap
        total = dict()

        for cutoff in boundaries:
            ap[cutoff] = []

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = {}
            temporary = sorted(interactions[query]['visited_documents_orders'].items(), key=lambda kv: (int(kv[1]), kv[0]))

            # for converting temporary to dict
            for element in temporary:
                visited_documents_orders[element[0]] = element[1]

            for cutoff in boundaries:
                pass_ = set(visited_documents)

                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        ap[cutoff].append({'value':0, 'count':0})
                        index = len(ap[cutoff])-1

                        for document in visited_documents_orders:
                            if document in pass_ and document in related_documents and int(visited_documents_orders[document]) <= cutoff:
                                ap[cutoff][index]['count'] += 1
                                ap[cutoff][index]['value'] += ap[cutoff][index]['count']/int(visited_documents_orders[document])

                                pass_ = pass_.difference([document])

                        ap[cutoff][index]['value'] /= len(related_documents)
                else:
                    ap[cutoff].append({'value': 0, 'count': 0})
                    index = len(ap[cutoff]) - 1

                    for document in visited_documents_orders:
                        if document in pass_ and document in related_documents:
                            ap[cutoff][index]['count'] += 1
                            ap[cutoff][index]['value'] += ap[cutoff][index]['count'] / int(visited_documents_orders[document])

                            pass_ = pass_.difference([document])

                    ap[cutoff][index]['value'] /= len(related_documents)

        # map calculation over all organised ap values
        for cutoff in boundaries:
            mean_ap[cutoff] = {'count': 0, 'value': 0}
            total[cutoff] = 0

            # is there any value for the related cutoff
            if len(ap[cutoff]) > 0:
                for i in range(len(ap[cutoff])):
                    total[cutoff] += ap[cutoff][i]['value']

                mean_ap[cutoff]['count'] = len(ap[cutoff])  # how many ap was used
                mean_ap[cutoff]['value'] = total[cutoff] / len(ap[cutoff])

        return mean_ap

    def gmap(self, interactions, constant=0.01, boundaries=['all']):
        ap = dict()
        gmap = dict() # geometric mean ap
        total = dict()

        for cutoff in boundaries:
            ap[cutoff] = []

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = {}
            temporary = sorted(interactions[query]['visited_documents_orders'].items(), key=lambda kv: (int(kv[1]), kv[0]))

            # for converting temporary to dict
            for element in temporary:
                visited_documents_orders[element[0]] = element[1]

            for cutoff in boundaries:
                pass_ = set(visited_documents)

                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        ap[cutoff].append({'value':0, 'count':0})
                        index = len(ap[cutoff])-1

                        for document in visited_documents_orders:
                            if document in pass_ and document in related_documents and int(visited_documents_orders[document]) <= cutoff:
                                ap[cutoff][index]['count'] += 1
                                ap[cutoff][index]['value'] += ap[cutoff][index]['count']/int(visited_documents_orders[document])

                                pass_ = pass_.difference([document])

                        ap[cutoff][index]['value'] /= len(related_documents)
                else:
                    ap[cutoff].append({'value': 0, 'count': 0})
                    index = len(ap[cutoff]) - 1

                    for document in visited_documents_orders:
                        if document in pass_ and document in related_documents:
                            ap[cutoff][index]['count'] += 1
                            ap[cutoff][index]['value'] += ap[cutoff][index]['count'] / int(visited_documents_orders[document])

                            pass_ = pass_.difference([document])

                    ap[cutoff][index]['value'] /= len(related_documents)

        # gmap calculation over all organised ap values
        for cutoff in boundaries:
            gmap[cutoff] = {'count': 0, 'value': 0}
            total[cutoff] = 1

            # is there any value for the related cutoff
            if len(ap[cutoff]) > 0:
                for i in range(len(ap[cutoff])):
                    if ap[cutoff][i]['value'] != 0:
                        total[cutoff] *= ap[cutoff][i]['value']+constant
                    else:
                        total[cutoff] *= constant

                gmap[cutoff]['count'] = len(ap[cutoff])  # how many ap was used
                gmap[cutoff]['value'] = pow(total[cutoff], 1/len(ap[cutoff]))

        return gmap

    def iap(self, interactions):
        iap = dict()
        ep = {'0.0': 0, '0.1': 0, '0.2': 0, '0.3': 0, '0.4': 0, '0.5': 0, '0.6': 0, '0.7': 0, '0.8': 0, '0.9': 0, '1.0': 0}
        p_iap = dict()

        index = 0
        for query in interactions:
            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = interactions[query]['visited_documents_orders']

            p_iap[index] = {'count': 0, 'rp': {}, 'ep': ep.copy()}
            for document_id in visited_documents:

                if document_id in related_documents:
                    p_iap[index]['count'] += 1

                    # calculation is stored as recall=>precision
                    recall = str(p_iap[index]['count'] / len(related_documents))
                    p_iap[index]['rp'][recall] = float(p_iap[index]['count'] / int(visited_documents_orders[document_id]))

            temporary = sorted(p_iap[index]['rp'].items(), key=lambda kv: (float(kv[0]), float(kv[1])), reverse=True)
            p_iap[index]['rp'] = {}

            for element in temporary:
                p_iap[index]['rp'][str(element[0])] = float(element[1])

            bprec = 0 # the biggest precision is going to be hold
            for recall in p_iap[index]['rp']:
                precision = p_iap[index]['rp'][recall]
                if bprec == 0:
                    bprec = precision

                if bprec < precision:
                    bprec = precision
                    p_iap[index]['rp'][recall] = bprec
                else:
                    p_iap[index]['rp'][recall] = bprec

            temporary = sorted(p_iap[index]['rp'].items(), key=lambda kv: (float(kv[0]), float(kv[1])))
            p_iap[index]['rp'] = {}
            for element in temporary:
                p_iap[index]['rp'][str(element[0])] = float(element[1])

            pass_ = set()
            for recall in p_iap[index]['rp']:
                precision = p_iap[index]['rp'][recall]
                for recall2 in p_iap[index]['ep']:
                    if recall2 not in pass_:
                        if float(recall2) <= float(recall):
                            p_iap[index]['ep'][recall2] = precision
                            pass_.add(recall2)
                        else:
                            break

            index += 1

        total = ep.copy()
        if len(p_iap) > 0:
            for i in range(len(p_iap)):
                for recall in p_iap[i]['ep']:
                    precision = p_iap[i]['ep'][recall]
                    total[recall] += precision

            for recall in total:
                precision = total[recall]
                iap[recall] = precision / len(p_iap)
        else:
            for recall in ep:
                iap[recall] = 0

        return iap

    def rprecision(self, interactions, boundaries=['all']):
        rprecision= dict()
        m_rprecision = dict() # mean rprecision

        for cutoff in boundaries:
            rprecision[cutoff] = []

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = interactions[query]['visited_documents_orders']

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        related = 0
                        for document_id in visited_documents:
                            if document_id in related_documents and int(visited_documents_orders[document_id]) <= cutoff:
                                related += 1

                        rprecision[cutoff].append(related/len(related_documents))
                else:
                    related = 0
                    for document_id in visited_documents:
                        if document_id in related_documents:
                            related += 1

                    rprecision[cutoff].append(related/len(related_documents))

        # mean rprecision calculation over all organised rprecision values
        for cutoff in boundaries:
            m_rprecision[cutoff] = {'count': 0, 'value': 0}

            # is there any value for the related cutoff
            if len(rprecision[cutoff]) > 0:
                m_rprecision[cutoff]['count'] = len(rprecision[cutoff])
                m_rprecision[cutoff]['value'] = sum(rprecision[cutoff]) / len(rprecision[cutoff])

        return m_rprecision

    def fmeasure(self, interactions, boundaries=['all']):
        fs= dict()
        fmeasure = dict()

        for cutoff in boundaries:
            fs[cutoff] = []

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            related_documents = interactions[query]['related_documents'] # the list of documents which is known that related to the query

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = interactions[query]['visited_documents_orders']

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        related = 0
                        for document_id in visited_documents:
                            if document_id in related_documents and int(visited_documents_orders[document_id]) <= cutoff:
                                related += 1

                        precision = related / cutoff
                        recall = related / len(related_documents)
                        p_plus_r = precision + recall

                        # 2 * precision * recall / precision + recall
                        if p_plus_r > 0:
                            fs[cutoff].append((2 * precision * recall) / p_plus_r)
                        else:
                            fs[cutoff].append(0)
                else:
                    related = 0
                    for document_id in visited_documents:
                        if document_id in related_documents:
                            related += 1

                    precision = related / total_result
                    recall = related / len(related_documents)
                    p_plus_r = precision + recall

                    # 2 * precision * recall / precision + recall
                    if p_plus_r > 0:
                        fs[cutoff].append((2 * precision * recall) / p_plus_r)
                    else:
                        fs[cutoff].append(0)

        # fmeasure calculation over all organised fs values
        for cutoff in boundaries:
            fmeasure[cutoff] = {'count': 0, 'value': 0}

            # is there any value for the related cutoff
            if len(fs[cutoff]) > 0:
                fmeasure[cutoff]['count'] = len(fs[cutoff]) # how many fs was used
                fmeasure[cutoff]['value'] = sum(fs[cutoff]) / len(fs[cutoff])

        return fmeasure

    def cgain(self, interactions, boundaries=['all']):
        cgain = dict()
        cg= dict()
        total = dict()

        for cutoff in boundaries:
            cg[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            orders = {}
            assessments = {}
            for document in assessed_documents:
                orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])
                counter += 1

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        index = len(cg[cutoff])
                        cg[cutoff][index] = 0

                        for i in range(1, cutoff+1):
                            key_ = [key for key, value in orders.items() if value == i]
                            if len(key_) > 0:
                                cg[cutoff][index] += assessments[key_[0]]
                else:
                    index = len(cg[cutoff])
                    cg[cutoff][index] = 0

                    for i in range(1, total_result + 1):
                        key_ = [key for key, value in orders.items() if value == i]
                        if len(key_) > 0:
                            cg[cutoff][index] += assessments[key_[0]]

        # cgain calculation over all organised cg values
        for cutoff in boundaries:
            cgain[cutoff] = {'count': 0, 'value': 0}
            total[cutoff] = 0

            # is there any value for the related cutoff
            if len(cg[cutoff]) > 0:
                for i in range(len(cg[cutoff])):
                    total[cutoff] += cg[cutoff][i]

                cgain[cutoff]['count'] = len(cg[cutoff]) # how many cg was used
                cgain[cutoff]['value'] = total[cutoff] / len(cg[cutoff])

        return cgain

    def ncgain(self, interactions, boundaries=['all']):
        ncgain = dict()
        ncg = dict()
        encg = dict()

        for cutoff in boundaries:
            ncg[cutoff] = {}
            encg[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            orders = {}
            assessments = {}
            temporary_expected_assessments = {}
            for document in assessed_documents:
                orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])
                temporary_expected_assessments[counter] = int(assessed_documents[document][1])
                counter += 1

            expected_assessments = {}
            temporary = sorted(temporary_expected_assessments.items(), key=lambda kv: (int(kv[1]), int(kv[0])), reverse=True)

            for element in temporary:
                expected_assessments[int(element[0])] = int(element[1])

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        index = len(ncg[cutoff])
                        ncg[cutoff][index] = 0
                        encg[cutoff][index] = 0

                        for i in range(1, cutoff+1):
                            key_ = [key for key, value in orders.items() if value == i]
                            if len(key_) > 0:
                                ncg[cutoff][index] += assessments[key_[0]]

                            if expected_assessments.get((i-1)) is not None:
                                encg[cutoff][index] += expected_assessments[(i-1)]
                else:
                    index = len(ncg[cutoff])
                    ncg[cutoff][index] = 0
                    encg[cutoff][index] = 0

                    for i in range(1, total_result + 1):
                        key_ = [key for key, value in orders.items() if value == i]
                        if len(key_) > 0:
                            ncg[cutoff][index] += assessments[key_[0]]

                        if expected_assessments.get((i - 1)) is not None:
                            encg[cutoff][index] += expected_assessments[(i - 1)]

        # ncgain calculation over all organised ncg values
        for cutoff in boundaries:
            ncgain[cutoff] = {'count': 0, 'value': 0}
            total = 0

            # is there any value for the related cutoff
            if len(ncg[cutoff]) > 0:
                for i in range(len(ncg[cutoff])):
                    total += ncg[cutoff][i] / encg[cutoff][i]

                ncgain[cutoff]['count'] = len(ncg[cutoff]) # how many ncg was used
                ncgain[cutoff]['value'] = total / len(ncg[cutoff])

        return ncgain

    def dcgain(self, interactions, boundaries=['all']):
        dcgain = dict()
        dcg= dict()

        for cutoff in boundaries:
            dcg[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            orders = {}
            assessments = {}
            for document in assessed_documents:
                orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])
                counter += 1

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        index = len(dcg[cutoff])
                        dcg[cutoff][index] = 0

                        for i in range(1, cutoff+1):
                            key_ = [key for key, value in orders.items() if value == i]
                            if len(key_) > 0:
                                if i == 1:
                                    dcg[cutoff][index] += assessments[key_[0]]
                                else:
                                    dcg[cutoff][index] += assessments[key_[0]] / math.log(i,2)
                else:
                    index = len(dcg[cutoff])
                    dcg[cutoff][index] = 0

                    for i in range(1, total_result + 1):
                        key_ = [key for key, value in orders.items() if value == i]
                        if len(key_) > 0:
                            if i == 1:
                                dcg[cutoff][index] += assessments[key_[0]]
                            else:
                                dcg[cutoff][index] += assessments[key_[0]] / math.log(i, 2)

        # dcgain calculation over all organised dcg values
        for cutoff in boundaries:
            dcgain[cutoff] = {'count': 0, 'value': 0}
            total = 0

            # is there any value for the related cutoff
            if len(dcg[cutoff]) > 0:
                for i in range(len(dcg[cutoff])):
                    total += dcg[cutoff][i]

                dcgain[cutoff]['count'] = len(dcg[cutoff]) # how many dcg was used
                dcgain[cutoff]['value'] = total / len(dcg[cutoff])

        return dcgain

    def ndcgain(self, interactions, boundaries=['all']):
        ndcgain = dict()
        dcg= dict()
        edcg = dict()

        for cutoff in boundaries:
            dcg[cutoff] = {}
            edcg[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            orders = {}
            assessments = {}
            temporary_expected_assessments = {}
            for document in assessed_documents:
                orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])
                temporary_expected_assessments[counter] = int(assessed_documents[document][1])
                counter += 1

            expected_assessments = {}
            temporary = sorted(temporary_expected_assessments.items(), key=lambda kv: (int(kv[1]), int(kv[0])), reverse=True)

            for element in temporary:
                expected_assessments[int(element[0])] = int(element[1])

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        index = len(dcg[cutoff])
                        dcg[cutoff][index] = 0
                        edcg[cutoff][index] = 0

                        for i in range(1, cutoff+1):
                            key_ = [key for key, value in orders.items() if value == i]
                            if len(key_) > 0:
                                if i == 1:
                                    dcg[cutoff][index] += assessments[key_[0]]
                                else:
                                    dcg[cutoff][index] += assessments[key_[0]] / math.log(i,2)

                            if i == 1:
                                if expected_assessments.get((i - 1)) is not None:
                                    edcg[cutoff][index] += expected_assessments[(i - 1)]
                            else:
                                if expected_assessments.get((i - 1)) is not None:
                                    edcg[cutoff][index] += expected_assessments[(i - 1)] / math.log(i, 2)
                else:
                    index = len(dcg[cutoff])
                    dcg[cutoff][index] = 0
                    edcg[cutoff][index] = 0

                    for i in range(1, total_result + 1):
                        key_ = [key for key, value in orders.items() if value == i]
                        if len(key_) > 0:
                            if i == 1:
                                dcg[cutoff][index] += assessments[key_[0]]
                            else:
                                dcg[cutoff][index] += assessments[key_[0]] / math.log(i, 2)

                        if i == 1:
                            if expected_assessments.get((i - 1)) is not None:
                                edcg[cutoff][index] += expected_assessments[(i - 1)]
                        else:
                            if expected_assessments.get((i - 1)) is not None:
                                edcg[cutoff][index] += expected_assessments[(i - 1)] / math.log(i, 2)

        # ndcgain calculation over all organised dcg values
        for cutoff in boundaries:
            ndcgain[cutoff] = {'count': 0, 'value': 0}
            total = 0

            # is there any value for the related cutoff
            if len(dcg[cutoff]) > 0:
                for i in range(len(dcg[cutoff])):
                    total += dcg[cutoff][i] / edcg[cutoff][i]

                ndcgain[cutoff]['count'] = len(dcg[cutoff]) # how many dcg was used
                ndcgain[cutoff]['value'] = total / len(dcg[cutoff])

        return ndcgain

    def mrr(self, interactions):
        total_inteaction = 0
        rr = 0

        for query in interactions:
            # first_visit: the order number of first visited page on the result list
            first_visit = int(interactions[query]['visited_documents_orders'][0])

            rr += 1 / first_visit
            total_inteaction += 1

        mrr = rr / total_inteaction

        return mrr

    def rbprecision(self, interactions, p=[0.5, 0.8, 0.95], boundaries=['all']):
        rbprecision = dict()
        m_rbprecision = dict() # mean rbprecision

        for cutoff in boundaries:
            rbprecision[cutoff] = {}
            m_rbprecision[cutoff] = {}
            for values in p:
                persistence = str(values)
                rbprecision[cutoff][persistence] = []
                m_rbprecision[cutoff][persistence] = {'count': 0, 'value': 0}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results

            # visited_documents: id of each visited page on the result list
            # the reason of using array_unique is to ignore the same page visits (happened repeatedly) in the same query
            temporary_visited_documents = interactions[query]['visited_documents']

            # temporary_visited_documents is converted to visited_documents by eleminating the same document_id's
            visited_documents = []
            for document_id in temporary_visited_documents:
                if document_id not in visited_documents:
                    visited_documents.append(document_id)

            # visited_documents_orders: the order of each visited page, which it's id is known, on the result list
            visited_documents_orders = {}
            temporary = sorted(interactions[query]['visited_documents_orders'].items(), key=lambda kv: (int(kv[1]), kv[0]))

            # for converting temporary to dict
            for element in temporary:
                visited_documents_orders[element[0]] = element[1]

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        for values in p:
                            pass_ = set(visited_documents)

                            persistence = str(values)
                            rbprecision[cutoff][persistence].append(0)
                            index = len(rbprecision[cutoff][persistence])-1

                            for document in visited_documents_orders:
                                if document in pass_ and int(visited_documents_orders[document]) <= cutoff:
                                    if int(visited_documents_orders[document]) == 1:
                                        rbprecision[cutoff][persistence][index] += 1
                                    else:
                                        rbprecision[cutoff][persistence][index] += pow(values, (int(visited_documents_orders[document])-1))

                                    pass_ = pass_.difference([document])

                            rbprecision[cutoff][persistence][index] *= (1-values)
                else:
                    for values in p:
                        pass_ = set(visited_documents)

                        persistence = str(values)
                        rbprecision[cutoff][persistence].append(0)
                        index = len(rbprecision[cutoff][persistence]) - 1

                        for document in visited_documents_orders:
                            if document in pass_:
                                if int(visited_documents_orders[document]) == 1:
                                    rbprecision[cutoff][persistence][index] += 1
                                else:
                                    rbprecision[cutoff][persistence][index] += pow(values, (int(visited_documents_orders[document]) - 1))

                                pass_ = pass_.difference([document])

                        rbprecision[cutoff][persistence][index] *= (1 - values)

        # mean rbprecision calculation over all organised rbprecision values
        for cutoff in boundaries:
            for values in p:
                persistence = str(values)

                # is there any value for the related cutoff
                if len(rbprecision[cutoff][persistence]) > 0:
                    m_rbprecision[cutoff][persistence]['count'] = len(rbprecision[cutoff][persistence])  # how many rbprecision was used
                    m_rbprecision[cutoff][persistence]['value'] = sum(rbprecision[cutoff][persistence]) / len(rbprecision[cutoff][persistence])

        return m_rbprecision

    def err(self, interactions, max_grade=5, boundaries=['all']):
        err = dict()
        m_err= dict() # mean err

        for cutoff in boundaries:
            err[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            temporary_orders = {}
            orders = {}
            assessments = {}
            for document in assessed_documents:
                temporary_orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])
                counter += 1

            temporary_sort = sorted(temporary_orders.items(), key=lambda kv: (int(kv[1]), int(kv[0])))

            for element in temporary_sort:
                orders[int(element[0])] = int(element[1])

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        temporary = {'rank': [], 'pvalue': []}
                        index = len(err[cutoff])
                        err[cutoff][index] = 0

                        for i in range(1, cutoff+1):
                            key_ = [key for key, value in orders.items() if value == i]
                            if len(key_) > 0:
                                temporary['rank'].append(1/i)
                                temporary['pvalue'].append((pow(2,assessments[key_[0]])-1) / pow(2,max_grade))

                        if len(temporary['rank']) > 0:
                            for i in range((len(temporary['rank'])-1),-1,-1):
                                others = 1

                                if i > 0:
                                    for j in range(i):
                                        others *= (1-temporary['pvalue'][j])

                                err[cutoff][index] += (temporary['rank'][i] * temporary['pvalue'][i] * others)
                else:
                    temporary = {'rank': [], 'pvalue': []}
                    index = len(err[cutoff])
                    err[cutoff][index] = 0

                    for i in range(1, total_result + 1):
                        key_ = [key for key, value in orders.items() if value == i]
                        if len(key_) > 0:
                            temporary['rank'].append(1 / i)
                            temporary['pvalue'].append((pow(2, assessments[key_[0]]) - 1) / pow(2, max_grade))

                    if len(temporary['rank']) > 0:
                        for i in range((len(temporary['rank']) - 1), -1, -1):
                            others = 1

                            if i > 0:
                                for j in range(i):
                                    others *= (1 - temporary['pvalue'][j])

                            err[cutoff][index] += (temporary['rank'][i] * temporary['pvalue'][i] * others)


        # m_err calculation over all organised err values
        for cutoff in boundaries:
            m_err[cutoff] = {'count': 0, 'value': 0}
            total = 0

            # is there any value for the related cutoff
            if len(err[cutoff]) > 0:
                for i in range(len(err[cutoff])):
                    total += err[cutoff][i]

                m_err[cutoff]['count'] = len(err[cutoff]) # how many err was used
                m_err[cutoff]['value'] = total / len(err[cutoff])

        return m_err

    def bpref(self, interactions, boundaries=['all']):
        bpref = dict()
        m_bpref= dict() # mean bpref

        for cutoff in boundaries:
            bpref[cutoff] = {}

        for query in interactions:
            total_result = int(interactions[query]['total_result']) # list: total count of results
            related_documents = []

            assessed_documents = interactions[query]['assessed_documents'] # the list of documents ,which is assesed by a specialist or a user, related to the query

            counter = 0
            tepmorary_orders = {}
            assessments = {}
            for document in assessed_documents:
                tepmorary_orders[counter] = int(assessed_documents[document][0])
                assessments[counter] = int(assessed_documents[document][1])

                if int(assessed_documents[document][1]) == 1:
                    related_documents.append(document)

                counter += 1

            orders = {}
            temporary = sorted(tepmorary_orders.items(), key=lambda kv: (int(kv[1]), kv[0]))

            # for converting temporary to dict
            for element in temporary:
                orders[element[0]] = element[1]

            for cutoff in boundaries:
                if isinstance(cutoff, int):
                    if total_result >= cutoff:
                        index = len(bpref[cutoff])
                        if len(related_documents) > 0:
                            bpref[cutoff][index] = 1/len(related_documents)
                            temp_calc = 0

                            for order in orders:
                                if orders[order] <= cutoff:
                                    counter = 0

                                    if assessments[order] == 1:
                                        for order2 in orders:
                                            if orders[order2] < orders[order]:
                                                if assessments[order2] == 0:
                                                    counter += 1
                                            else:
                                                break

                                        temp_calc += (1 - (counter / len(related_documents)))
                                else:
                                    break

                            bpref[cutoff][index] *= temp_calc
                        else:
                            bpref[cutoff][index] = 0
                else:
                    index = len(bpref[cutoff])
                    if len(related_documents) > 0:
                        bpref[cutoff][index] = 1 / len(related_documents)
                        temp_calc = 0

                        for order in orders:
                            counter = 0

                            if assessments[order] == 1:
                                for order2 in orders:
                                    if orders[order2] < orders[order]:
                                        if assessments[order2] == 0:
                                            counter += 1
                                    else:
                                        break

                                temp_calc += (1 - (counter / len(related_documents)))

                        bpref[cutoff][index] *= temp_calc
                    else:
                        bpref[cutoff][index] = 0

        # mean bpref calculation over all organised bpref values
        for cutoff in boundaries:
            m_bpref[cutoff] = {'count': 0, 'value': 0}
            total = 0

            # is there any value for the related cutoff
            if len(bpref[cutoff]) > 0:
                for i in range(len(bpref[cutoff])):
                    total += bpref[cutoff][i]

                m_bpref[cutoff]['count'] = len(bpref[cutoff]) # how many bpref was used
                m_bpref[cutoff]['value'] = total / len(bpref[cutoff])

        return m_bpref